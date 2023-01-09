#!/usr/bin/env groovy

pipeline {
    agent {
        docker {
            // image 'ultralytics/yolov5:latest'
            image 'hoangchieng282/mlops_image:v1'
            args '--ipc=host'
        }
    }

    parameters {
        string(name: 'IMG', description: 'The image size for training. Example 480', defaultValue: "480")
        string(name: 'BATCH', description: 'The number to build at a time. Example 1', defaultValue: "1")
        string(name: 'EPOCH', description: 'The number of training for model. Example 1', defaultValue: "1")
        string(name: 'DATA_PATH', description: 'The path to data folder. Example mlops-demo-project-1', defaultValue: "mlops-demo-project-1")
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    // environment {
    //     // Copy the Jenkins build number of Suite-Build job into a global iPension environment variable
    //     // IPENSION_BUILD_NUMBER = "${env.BUILD_NUMBER}"

    // }

    stages {
        
        stage('Initial data') {
            steps {
                sh '''
                    python --version
                    python initial_data/runs.py
                '''
                
                // script {

                // }
            }
        }
        stage('check'){
            steps {
                sh ''' ls '''
            }
        }
        stage('Training model') {
            steps {
                sh '''
                    python train.py --img 480 --batch 1 --epochs 1 --data mlops-demo-project-1/data.yaml --weights yolov5l.pt
                '''
            }

        }

        stage('Build torchserve image'){
            steps {
                echo "build"
            }
        }

    }
        post {
            always {
                cleanWs()
            }
        }

}