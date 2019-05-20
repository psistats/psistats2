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
                stage("Python 3.5") {
                    agent { label 'master' }
                    steps {
                        sh 'tox -e py35 --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-py35'                            
                    }
                }

                stage("Python 3.6") {
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
                    environment {
                        PATH = "C:\\Users\\moogle\\jenkins\\workspace\\psistats2_develop\\env\\Scripts;${env.PATH}"
                    }                    
                    steps {
                        bat 'virtualenv env'
                        bat 'pip install -r requirements_win.txt'
                        bat 'building\\windows\\build.bat'
                        zip zipFile: 'dist\\psistats2.zip', dir: 'dist\\psistats2'
                        archiveArtifacts artifacts: 'dist/psistats2.zip', fingerprint: true
                    }
                }
            }
        }
    }

    post {
        always {
            emailext subject: "[PsikonCI] ${env.JOB_NAME} - ${env.BUILD_STATUS}",
                     body: "${env.BUILD_URL}",
                     to: "ci@psikon.com",
                     recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
        }
    }
}
