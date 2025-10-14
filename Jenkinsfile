pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'booklib-api'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DEPLOY_SERVER = '192.168.1.175'
        DEPLOY_USER = 'deploy'
        DEPLOY_PATH = '/opt/booklib/api'
        REGISTRY = 'localhost:5000' // Optional: use if you have a private registry
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
        
        stage('Save Docker Image') {
            steps {
                script {
                    sh """
                        docker save ${DOCKER_IMAGE}:latest | gzip > ${DOCKER_IMAGE}.tar.gz
                    """
                }
            }
        }
        
        stage('Deploy to Server') {
            steps {
                sshagent(['deploy-key']) {
                    sh """
                        # Ensure deploy path exists
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} 'mkdir -p ${DEPLOY_PATH}'

                        # Copy docker image to deploy server
                        scp -o StrictHostKeyChecking=no ${DOCKER_IMAGE}.tar.gz ${DEPLOY_USER}@${DEPLOY_SERVER}:/tmp/

                        # Copy deployment files
                        scp -o StrictHostKeyChecking=no docker-compose.yml ${DEPLOY_USER}@${DEPLOY_SERVER}:${DEPLOY_PATH}/
                        scp -o StrictHostKeyChecking=no .env.test.example ${DEPLOY_USER}@${DEPLOY_SERVER}:${DEPLOY_PATH}/
                        
                        # Deploy on remote server
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} '
                            cd ${DEPLOY_PATH}
                            
                            # Load docker image
                            docker load < /tmp/${DOCKER_IMAGE}.tar.gz
                            
                            # Ensure external network exists
                            docker network inspect booklib-net >/dev/null 2>&1 || docker network create booklib-net

                            # Create .env file if it doesn't exist
                            if [ ! -f .env.test ]; then
                                cp .env.test.example .env.test
                                echo "WARNING: Please update .env.test with secure credentials!"
                            fi
                            
                            # Stop old containers
                            docker compose -f ${DEPLOY_PATH}/docker-compose.yml down || true
                            
                            # Start new containers
                            docker compose -f ${DEPLOY_PATH}/docker-compose.yml --env-file ${DEPLOY_PATH}/.env.test up -d
                            
                            # Wait for API to be healthy
                            echo "Waiting for API to be healthy..."
                            for i in {1..30}; do
                                if curl -f http://localhost:5000/health; then
                                    echo "API is healthy!"
                                    break
                                fi
                                echo "Attempt \$i: API not ready yet..."
                                sleep 2
                            done
                            
                            # Cleanup
                            rm -f /tmp/${DOCKER_IMAGE}.tar.gz
                            
                            # Show container status
                            docker compose ps
                        '
                    """
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    def result = sh(
                        script: """
                            set +e
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} '
                                echo "Running API health check..."
                                curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health || echo "curl failed"
                            '
                        """,
                        returnStatus: true
                    )
                    echo "Health check stage completed with exit code ${result} (ignored)."
                }
            }
        }    
    }
    post {
        success {
            echo "Deployment to ${DEPLOY_SERVER} completed successfully!"
        }
        failure {
            echo "Deployment failed. Please check the logs."
            script {
                sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} '
                        cd ${DEPLOY_PATH}
                        docker compose logs --tail=50 api || true
                    '
                """
            }
        }
        always {
            // Cleanup workspace
            sh "rm -f ${DOCKER_IMAGE}.tar.gz"
            cleanWs()
        }
    }
}
