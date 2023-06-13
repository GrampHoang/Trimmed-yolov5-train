#!/usr/bin/env groovy
library 'mlops-shared-lib'

def dockerBuild(String branch, String stageName,String trainNumber, String stageResult = false, String propagate = true) {
    try {
        // Launch the job that builds iPension Suite
        build job: branch,
                parameters: [
                    string(name: 'TRAINNUMBER', value: trainNumber)
                ],
                propagate: propagate
        stageResult = true
        return stageResult
    }
    catch (Exception e) {
        unstable(stageName + " failed!")
        currentBuild.result = 'FAILURE'
        stageResult = false
        return stageResult
    }
}

pipeline {
    agent {
        docker {
            // image 'ultralytics/yolov5:latest'
            image 'hoangchieng/mlops_image:v3'
            args '--ipc=host'
        }
    }

    parameters {
        string(name: 'MODEL_NAME', description: 'The name for the model')
        string(name: 'DATA_URL', description: 'The URL to load the dataset from Roboflow')
        string(name: 'IMG', description: 'The image size for training. Example 480', defaultValue: "480")
        string(name: 'BATCH', description: 'The number to build at a time. Example 1', defaultValue: "1")
        string(name: 'EPOCH', description: 'The number of training for model. Example 1', defaultValue: "1")
        string(name: 'WEIGHT', description: 'The weight to start traing from. Example yolov5l.pt', defaultValue: "yolov5n.pt")
    }
    options {
        timeout(time: 22, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        def SERVER_ID="Jfrog-mlops-model-store"
        // Copy the Jenkins build number of Suite-Build job into a global iPension environment variable
        def ARCHIV = "${params.MODEL_NAME}"+'.tar.gz'
        def WEIGHT_PATH = "${params.WEIGHT}"
        // Define default job parameters
        def model_weight=""
        def useYoloModel=true
        propagate = true

    }

    stages {
        
        stage("Precheck pipeline parameters"){
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'artifactory-chih',
                            usernameVariable: 'USERNAME',
                            passwordVariable: 'PASSWORD'
                        )
                    ]){
                        echo "Validating parameters..."
                        if (!params.MODEL_NAME?.trim()) {
                            error "MODEL_NAME is a mandatory parameter"
                            return
                        }
                            if (!params.DATA_URL?.trim()) {
                            error "DATA_URL is a mandatory parameter"
                            return
                        }
                        //Check semantic rule for parameter
                        semanticVersionCheck(this,params.MODEL_NAME)
                        
                        echo "Checking the weight to be trained from"
                        if (!WEIGHT_PATH.contains("yolo")){
                            model_weight= WEIGHT_PATH.split(':')
                            if(model_weight.size() == 2){
                                sh "echo Checking on model: ${WEIGHT_PATH}"
                                sh "curl -u ${USERNAME}:${PASSWORD} -f -I https://${env.SERVER_URL}/artifactory/${env.MODEL_REPO}/${model_weight[0]}/${model_weight[1]}.tar.gz"
                                useYoloModel=false
                            }else {
                                error "weight input failed!"
                                return 
                            }
                        }
                    }
                }
            }
        }

        stage("Get weight to train from"){
            when {
                expression {
                    return !useYoloModel
                }
            }
            steps {             
                script {
                    def server = Artifactory.server(SERVER_ID)                   
                    sh "echo Download model: ${model_weight[0]} version: ${model_weight[1]}"                       
                        // Perform the desired steps for each value
                    def downloadSpec = """{
                            "files": [
                                {
                                    "pattern": "${env.MODEL_REPO}/${model_weight[0]}/${model_weight[1]}.tar.gz",
                                    "target": "./"
                                }
                            ]
                    }"""
                    def buildInfo = server.download(downloadSpec)
                    sh """
                            cd ${model_weight[0]}
                            chmod 777 ${model_weight[1]}.tar.gz
                            tar -xvf ${model_weight[1]}.tar.gz
                            mv train/exp/weights/best.pt ../${model_weight[0]}.pt
                            
                        """
                    sh "chmod 777 ${model_weight[0]}.pt"
                    WEIGHT_PATH="${model_weight[0]}.pt"
                }
            }
        }

        stage('Initial training data') {
            steps {             
                script {
                    sh "python --version"
                    sh "curl -f -L ${params.DATA_URL} > roboflow.zip"
                }
            }
            post {
                success {
                    script { 
                        unzip zipFile: "roboflow.zip", quiet: true
                        sh "chmod -R 777 .; rm roboflow.zip"
                    }
                }
            }
        }

        stage('Training model') {
            steps {
                script {
                    sh "python train.py --img ${params.IMG} --batch ${params.BATCH} --epochs ${params.EPOCH} --data data.yaml --weights ${WEIGHT_PATH}"
                }
            }
            post {
                success {
                    script { 
                        tar file: ARCHIV, archive: true, dir: 'runs' 
                    }
                }
            }
        }


        stage('Upload model and results to Artifactory') {
            steps {
                script {
                    MY_DATE_TIME = sh(returnStdout: true, script: 'date +%d%m%y%H').trim()

                    rtUpload (
                        serverId: 'Jfrog-mlops-model-store', 
                        spec: """{
                            "files": [
                                {
                                    "pattern": "${ARCHIV}", 
                                    "target": "${env.MODEL_REPO}/${MODEL_NAME}/${MY_DATE_TIME}.tar.gz"
                                }
                            ]
                        }"""
                    )

                    rtUpload (
                        serverId: 'Jfrog-mlops-model-store', 
                        spec: """{
                            "files": [
                                {
                                    "pattern": "${ARCHIV}", 
                                    "target": "${env.MODEL_REPO}/${MODEL_NAME}/latest.tar.gz"
                                }
                            ]
                        }"""
                    )

                    sh "python ./mongo_config/InsertModel.py --resultFilePath ./runs/train/exp/opt.yaml --modelName ${MODEL_NAME} --img ${params.IMG} --batch ${params.BATCH} --epochs ${params.EPOCH} --version ${MY_DATE_TIME} --weightFile ${params.WEIGHT} --dataUrl ${params.DATA_URL} --outputFile output.json"
                }
            }
            success {
                sh "python ./mongo_config/UpdateTrainResult.py --modelName ${MODEL_NAME} --status success"
            }

            failure {
                sh "python ./mongo_config/UpdateTrainResult.py --modelName ${MODEL_NAME} --status fail"
            }
        }

    }
    post {
        success {
            slackSend(color:"good", message:"To: <!here|here>, Build deployed successfully - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
            sh "python ./mongo_config/UpdateTrainResult.py --modelName ${MODEL_NAME} --status success"
        }

        failure {
            slackSend(color:"#ff0000",message: "To: <!channel|channel>, Build failed  - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
            sh "python ./mongo_config/UpdateTrainResult.py --modelName ${MODEL_NAME} --status fail"
        }

        always {
            cleanWs()
        }
    }
}