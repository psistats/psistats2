pipeline {

    agent any
    stages {
        stage("Prepare") {
            steps {
                emailext body: 'Job Starting test', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: 'Job Start'
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
            }
        }
    }

    post {
        always {
            emailext body: 'Post Always: A Test EMail', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: 'Job Done'
        }
    }
}
