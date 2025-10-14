pipeline {
    agent any
    environment {
        PYTHONPATH = '.'
    }
    stages {
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
