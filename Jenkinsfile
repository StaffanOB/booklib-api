pipeline {
    agent any
    environment {
        PYTHONPATH = '.'
    }
    stages {
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
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
