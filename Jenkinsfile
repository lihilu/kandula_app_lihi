pipeline {
    agent {label "jenkins1"}
        environment {
            register = "lihilure/kandula_image_app"
            dockerimage = ""
            AWS_DEFAULT_REGION="us-east-1"
            upload_image = "${register}:${params.Version}-${env.BUILD_NUMBER}"
        }
        parameters {
            gitParameter ( 
                    branch: 'new',
                    branchFilter: ".*",
                    defaultValue: "new",
                    description: '',
                    listSize: '10',
                    name: 'Version',
                    quickFilterEnabled: false,
                    selectedValue: 'NONE',
                    sortMode: 'ASCENDING_SMART',
                    tagFilter: "*",
                    type: 'PT_TAG')
        }
    stages {
        stage('slack massage') {
            steps{
                script{
                    channel = "_notifications"
                    slackSend channel: channel,  color: "#6a0dad", message: "Build Started: ${env.JOB_NAME} ${env.BUILD_NUMBER} Version:${params.Version} "
                    end = "failure"
                    customImage = ""}
                }
        }

        stage("git clone") {
            steps{
                script {

                    end = "failure"
                    git branch:'new', credentialsId: 'a4f8a586-5917-4b6b-bcdb-eca9865e558f', url: 'https://github.com/lihilu/kandula_app_lihi.git'
                    end = "success"
                }
            }
        }
        stage("update yaml file") {
            steps{
                script {
                    sh "sed -i 's/TAG/${params.Version}-${env.BUILD_NUMBER}/' deployment_kandula_app.yaml"
                    sh "cat deployment_kandula_app.yaml"
                }
            }
        }
        stage("create docker build") {
            steps{
                script {
                    end = "failure"
                    dockerimage = docker.build register + ":${params.Version}-${env.BUILD_NUMBER}" 
                     end = "success"
                }
            }    
        }
        stage("scan image"){
            steps{
                echo "Scanning image ${upload_image}"
                sh "trivy image --timeout 5m --severity CRITICAL,HIGH ${upload_image}"
                sh "trivy image --timeout 5m --severity UNKNOWN,LOW,MEDIUM ${upload_image}"
            }
        }
        stage("docker push"){
            steps{
                script{
                    end = "failure"
                    withDockerRegistry([ credentialsId: "lihi_dockerhub", url: "" ]) {
                    sh "docker image push ${upload_image}"
                    }
                    end = "success"
                }
            }    
        }
        stage("delete docker") {
           steps{
                script {
                    end = "failure"
                    sh " docker image prune -a --force"
                    end = "success"
                }
           }
        }
        stage("connect to kubernetes") {
           steps{
                script {
                    end = "failure"
                    sh 'aws eks --region=us-east-1 update-kubeconfig --name kandula-project-eks'
                    sh 'aws sts get-caller-identity'
                    end = "success"
                }
           }
        }
        stage("deploy app on kubernetes") {
           steps{
                script {
                    end = "failure"
                    withCredentials([usernamePassword(credentialsId: 'awslogin', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                        sh 'kubectl apply -f deployment_kandula_app.yaml -n kandula'
                        sh 'kubectl apply -f /tmp/kubenlb.yaml -n kandula'
                    }
                    end = "success"
                }
           }
        }
        
    }
    post{
        always{
            script{
                if (end == "success"){
                     slackSend channel: channel, color: "#00FF00", message: "Build ended successfully: ${env.JOB_NAME} ${env.BUILD_NUMBER} Version:${params.Version}"
                     slackSend channel: channel,  color: "#00FF00", message: "results: ${env.BUILD_URL}"}
                else{
                     slackSend channel: channel, color: "#FF0000", message: "Build ended with errors: ${env.JOB_NAME} ${env.BUILD_NUMBER} Version:${params.Version}"
                     slackSend channel: channel, color: "#FF0000", message: "results: ${env.BUILD_URL}"}

            }

        }
    }
}