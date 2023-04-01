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
        string(name: 'IMG', description: 'The image size for training. Example 480', defaultValue: "480")
        string(name: 'BATCH', description: 'The number to build at a time. Example 1', defaultValue: "1")
        string(name: 'EPOCH', description: 'The number of training for model. Example 1', defaultValue: "1")
        string(name: 'DATA_PATH', description: 'The path to data folder. Example mlops-demo-project-1', defaultValue: "mlops-demo-project-1")
        string(name: 'WEIGHT', description: 'The weight to start traing from. Example yolov5l.pt', defaultValue: "yolov5n.pt")
    }
    options {
        timeout(time: 1, unit: 'HOURS')
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
        
        stage('Initial training data') {
            steps {
                sh '''
                    python --version
                    python initial_data/runs.py
                '''
            }
        }

        stage('Training model') {
            steps {
                sh "python train.py --img ${params.IMG} --batch ${params.BATCH} --epochs ${params.EPOCH} --data ${params.DATA_PATH}/data.yaml --weights ${params.WEIGHT}"
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
                rtUpload (
                    serverId: 'my-artifactory-server', 
                    spec: """{
                        "files": [
                            {
                                "pattern": "${ARCHIV}", 
                                "target": "mlops-trained-model/${latest}.tar.gz"
                            }
                        ]
                    }"""
                )
            }
        }

    }
    post {
        always {
            cleanWs()
        }
    }
}