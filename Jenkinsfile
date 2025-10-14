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
              sshagent(['deploy-key']) {
                sh '''
                  ssh -o StrictHostKeyChecking=no deploy@192.168.1.175 '
                    cd /opt/booklib &&
                    docker compose pull &&
                    docker compose up -d
                  '
                '''
              }
            }
        }
    }
}
