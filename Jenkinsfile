pipeline {

    agent any

    stages {

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
    }
}
