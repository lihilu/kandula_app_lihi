pipeline {
    environment {
        docker_image_name= "lihilure/kandula_image_app"
        docker_image= ""
    }
    agent any

    stage {
        stage('checkout source') {
            step {
                git 'https://github.com/lihilu/kandule_app_lihi.git'
            }
        }
        stage ('Build image') {
            environment {
                registryCredentials= 'lihi dockerhub'
            }
            step {
                script {
                    docker.withRegistry('https://registry.docker.com', registryCredentials) {
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