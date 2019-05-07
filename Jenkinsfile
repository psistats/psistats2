pipeline {

    agent any

    stages {
        stage("Python 3.5 Unit Tests") {
            steps {
                try {
                    sh 'tox -e py35 --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-py35'
                } catch(e) {
                    emailext(
                        subject: "FAILED: '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                        body: "${env.BUILD_URL}",
                        recipientProviders: [[$class: 'DevelopersRecipientProvider']]
                    )
                }
                        
            }
        }

        stage("Python 3.6 Unit Tests") {
            steps {
                sh 'tox -e py36 --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-py36'
            }
        }
    }
}
