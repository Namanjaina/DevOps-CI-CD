pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Namanjaina/DevOps-CI-CD.git'
            }
        }

        stage('Test') {
            steps {
                echo 'Hello DevOps 🚀'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t devops-app .'
            }
        }

        stage('Run Docker') {
            steps {
                sh 'docker rm -f devops-app-container || true'
                sh 'docker run -d --name devops-app-container -p 8000:8000 devops-app'
            }
        }
    }
}
