#!/usr/bin/env groovy

pipeline {
    agent {
        docker {
            // image 'ultralytics/yolov5:latest'
            image 'hoangchieng282/mlops_image:v1'
            args '--ipc=host'
        }
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
}