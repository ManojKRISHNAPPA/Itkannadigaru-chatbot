pipeline {
    agent any
    
    environment {
        IMAGE_NAME   = "manojkrishnappa/itkannadigaru-chat-bot:${GIT_COMMIT}"
        AWS_REGION   = "us-west-2"
        CLUSTER_NAME = "itkannadigaru-cluster"
        NAMESPACE    = "itkannadigaru"
    }

    stages {

        stage('Git-checkout') {
            steps {
                git url: 'https://github.com/ManojKRISHNAPPA/Itkannadigaru-chatbot.git', branch: 'main'
            }
        }

        stage('Building-Stage') {
            steps {
                sh '''
                    printenv
                    docker build -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }

        stage('Pushing to Docker hub') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}
                '''
            }
        }

        stage('Cluster-Update') {
            steps {
                sh '''
                    aws eks update-kubeconfig \
                      --region ${AWS_REGION} \
                      --name ${CLUSTER_NAME}
                '''
            }
        }

        stage('Deploying to EKS clsuter') {
            steps {
                withKubeConfig(
                    caCertificate: '',
                    clusterName: 'itkannadigaru-cluster',
                    contextName: '',
                    credentialsId: 'kube',
                    namespace: 'itkannadigaru',
                    restrictKubeConfigAccess: false,
                    serverUrl: 'https://F615C73A299CF72C4FB48A839E43EA9D.gr7.us-west-2.eks.amazonaws.com'
                ) {
                    sh "sed -i 's|replace|${IMAGE_NAME}|g' Deployment.yml"
                    sh "kubectl apply -f Deployment.yml -n ${NAMESPACE}"
                }
            }
        }

        stage('Verify the deployment') {
            steps {
                withKubeConfig(
                    caCertificate: '',
                    clusterName: 'itkannadigaru-cluster',
                    contextName: '',
                    credentialsId: 'kube',
                    namespace: 'itkannadigaru',
                    restrictKubeConfigAccess: false,
                    serverUrl: 'https://F615C73A299CF72C4FB48A839E43EA9D.gr7.us-west-2.eks.amazonaws.com'
                ) {
                    sh "kubectl get pods -n ${NAMESPACE}"
                    sh "kubectl get svc -n ${NAMESPACE}"
                }
            }
        }
    }
}
