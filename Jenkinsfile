pipeline {

    agent any
    stages {
        stage("Prepare") {
            steps {
                emailext subject: "[PsikonCI ${env.JOB_NAME} - Started",
                         body: "${env.BUILD_URL}",
                         to: "ci@psikon.com",
                         recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
            }
        }

        stage("Python 3.5 Unit Tests") {
            steps {
                sh 'tox -e py35 --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-py35'                            
            }
        }

        stage("Python 3.6 Unit Tests") {
            steps {
                sh 'tox -e py36 --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-py36'
            }
        }
    
        stage("Build Debian Artifact") {
            steps {
                sh 'building/debian/python_pkg.sh'
                archiveArtifacts artifacts: 'dist/debian_output/*.deb', fingerprint: true
                sh 'aptly repo add psikon-devel dist/debian_output/*.deb'
                sh '~/debian_repo/update.sh'
            }

        }
    }

    post {
        always {
            emailext subject: "[PsikonCI ${env.JOB_NAME} - Finished",
                     body: "${env.BUILD_URL}",
                     to: "ci@psikon.com",
                     recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
        }
    }
}
