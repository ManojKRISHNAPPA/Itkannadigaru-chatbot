pipeline{
    agent any
    
    environment{
        IMAGE_NAME = "manojkrishnappa/itkannadigaru-chat-bot:${GIT_COMMIT}"
    }

    stages{
        stage('Git-checkout'){
            steps{
                git url: 'https://github.com/ManojKRISHNAPPA/Itkannadigaru-chatbot.git',branch: 'main'
            } 
        }
        stage('Building-Stage'){
            steps{
                sh '''
                    printenv
                    docker build -t ${IMAGE_NAME} .
                '''
            } 
        }
        stage('Testing-Stage'){
            steps{
                sh '''
                    docker kill itkannadigaru-chat-bot
                    docker rm itkannadigaru-chat-bot
                    docker run -it -d --name itkannadigaru-chat-bot -p 9001:8501 ${IMAGE_NAME}
                '''
            } 
        }
        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        // Login to Docker Hub
                        sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
                    }
                }
            }
        }

        stage('Pushing to Docker hub'){
            steps{
                sh '''
                    docker push ${IMAGE_NAME}
                '''
            }
        }
    }

}