#!/usr/bin/env groovy

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
        // Copy the Jenkins build number of Suite-Build job into a global iPension environment variable
        MLOPS_TRAIN_NUMBER = "${env.BUILD_NUMBER}"
        ARCHIV = "${params.MODEL_NAME}"+'.tar.gz'
        // Define default job parameters
        propagate = true

    }

    stages {
        
        stage("Precheck pipeline parameters"){
            steps {
                script {
                    echo "Validating parameters..."
                    if (!params.MODEL_NAME?.trim()) {
                        error "MODEL_NAME is a mandatory parameter"
                        return
                    }
                        if (!params.DATA_URL?.trim()) {
                        error "DATA_URL is a mandatory parameter"
                        return
                    }
                }
            }
        }

        stage('Initial training data') {
            steps {
                sh "python --version"
                sh "curl -f -L ${params.DATA_URL} > roboflow.zip"
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
                    sh "python train.py --img ${params.IMG} --batch ${params.BATCH} --epochs ${params.EPOCH} --data data.yaml --weights ${params.WEIGHT}"
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
                                    "target": "mlops-trained-models/${MODEL_NAME}/${MY_DATE_TIME}.tar.gz"
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
                                    "target": "mlops-trained-models/${MODEL_NAME}/latest.tar.gz"
                                }
                            ]
                        }"""
                    )

                    sh "python ./mongo_config/InsertModel.py --resultFilePath ./runs/train/exp/opt.yaml --modelName ${MODEL_NAME} --img ${params.IMG} --batch ${params.BATCH} --epochs ${params.EPOCH} --version ${MY_DATE_TIME}"
                }
            }
        }

    }
    post {
        success {
            slackSend(color:"good", message:"To: <!here|here>, Build deployed successfully - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }

        failure {
            slackSend(color:"#ff0000",message: "To: <!channel|channel>, Build failed  - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }

        always {
            cleanWs()
        }
    }
}