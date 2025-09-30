pipeline {
    agent any

    environment {
        IMAGE_NAME = "ecomm-app"
        CONTAINER_NAME = "ecomm-app-container"
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning Git repository...'
                git 'https://github.com/syedtalhahamid/Ecommerce_Application.git' // replace with your repo
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    if (isUnix()) {
                        sh "docker build -t ${IMAGE_NAME}:${DOCKER_TAG} ."
                    } else {
                        bat "docker build -t ${IMAGE_NAME}:${DOCKER_TAG} ."
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                echo 'Running Docker container...'
                script {
                    if (isUnix()) {
                        sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}:${DOCKER_TAG}"
                    } else {
                        bat "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}:${DOCKER_TAG}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
