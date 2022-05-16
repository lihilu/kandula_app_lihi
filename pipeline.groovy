pipeline {
    environment {
        docker_image_name= "lihilure/kandula_image_app"
        docker_image= ""
    }
    agent any

    stages {
        stage('checkout source') {
            steps {
                git branch: 'main', credentialsId: 'Lihi.opsschool.jenkins', url: 'https://github.com/lihilu/kandule_app_lihi.git'
            }
        }
        stage ('Build image') {
            environment {
                registryCredentials= 'lihi dockerhub'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredentials) {
                        dockerImage.push("latest")
                    }
                }
            }

        }
    stage ('Deploying App to kubernetes') {
        steps {
            script {
                kubernetesDeploy(configs: "kandula_app.yaml", kubeconfigId: "kubernetes")
            }
        }
    }
    }
}