pipeline{
    agent any
    
    environment{
        IMAGE_NAME = "itkannadigaru-chat-bot:${GIT_COMMIT}"
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
                    docker run -it -d --name itkannadigaru-chat-bot -p 9001:8501 ${IMAGE_NAME}
                '''
            } 
        }
    }

}