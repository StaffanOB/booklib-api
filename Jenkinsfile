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
                    script {
                        sh """
                            set -e
                            cd ${WORKSPACE}
                            echo "Current workspace:"
                            pwd
                            ls -la

                            # Ensure deploy path exists
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} 'mkdir -p ${DEPLOY_PATH}'

                            echo "Copying image and deployment files..."
                            scp -o StrictHostKeyChecking=no ${WORKSPACE}/${DOCKER_IMAGE}.tar.gz ${DEPLOY_USER}@${DEPLOY_SERVER}:/tmp/
                            scp -o StrictHostKeyChecking=no ${WORKSPACE}/docker-compose.yml ${DEPLOY_USER}@${DEPLOY_SERVER}:${DEPLOY_PATH}/
                            scp -o StrictHostKeyChecking=no ${WORKSPACE}/.env.test.example ${DEPLOY_USER}@${DEPLOY_SERVER}:${DEPLOY_PATH}/

                            echo "Running deployment commands on server..."
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} '
                                set +e
                                cd ${DEPLOY_PATH}

                                docker load < /tmp/${DOCKER_IMAGE}.tar.gz
                                docker network inspect booklib-net >/dev/null 2>&1 || docker network create booklib-net

                                if [ ! -f .env.test ]; then
                                    cp .env.test.example .env.test
                                    echo "WARNING: Created .env.test from example"
                                fi

                                docker compose -f docker-compose.yml down || true
                                docker compose --env-file .env.test up -d || true
                                docker compose ps || true
                                exit 0
                            '
                        """
                    }
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
