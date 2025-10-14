pipeline {
    agent any
    environment {
        PYTHONPATH = '.'
    }
    stages {
        stage('Test') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -v tests/'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t booklib-api .' 
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploy stage (customize for your environment)'
            }
        }
    }
}
