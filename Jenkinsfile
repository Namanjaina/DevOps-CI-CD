pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Namanjaina/DevOps-CI-CD.git'
            }
        }

        stage('Test') {
            steps {
                echo 'Hello DevOps 🚀'
            }
        }

        stage('Build Docker') {
            steps {
                bat 'docker build -t devops-app .'
            }
        }

        stage('Run Docker') {
            steps {
                bat 'docker rm -f devops-app-container || exit 0'
                bat 'docker run -d --name devops-app-container -p 8000:8000 devops-app'
            }
        }
    }
}
