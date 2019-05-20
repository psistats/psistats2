pipeline {

    agent { label 'master' }
    stages {
        stage("Prepare") {
            steps {
                emailext subject: "[PsikonCI] ${env.JOB_NAME} - Started",
                         body: "${env.BUILD_URL}",
                         to: "ci@psikon.com",
                         recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
            }
        }

        stage('Unit Tests') {
            
            parallel {
                stage("Python 3.5 Unit Tests") {
                    agent { label 'master' }
                    steps {
                        sh 'tox -e py35 --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-py35'                            
                    }
                }

                stage("Python 3.6 Unit Tests") {
                    agent { label 'master' }
                    steps {
                        sh 'tox -e py36 --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-py36'
                    }
                }                
            }
        }

        stage('Build Artifacts') {
            parallel {
                stage('Debian') {
                    agent { label 'master' }
                    steps {
                        sh 'building/debian/python_pkg.sh'
                        archiveArtifacts artifacts: 'dist/debian_output/*.deb', fingerprint: true
                        sh 'aptly repo add psikon-devel dist/debian_output/*.deb'
                        sh '~/debian_repo/update.sh'                        
                    }
                }
                stage('Windows') {
                    agent { label 'windows' }
                    steps {
                        sh """
                        virtualenv env -p python3
                        env\\Scripts\\activate.bat
                        pip install -r requirements_win.txt
                        building\\windows\\build.bat
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            emailext subject: "[PsikonCI] ${env.JOB_NAME} - Finished",
                     body: "${env.BUILD_URL}",
                     to: "ci@psikon.com",
                     recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
        }
    }
}
