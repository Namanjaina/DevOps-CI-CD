pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        APP_NAME = 'devops-app'
        CONTAINER_NAME = 'devops-app-container'
        HOST_PORT = '8000'
        CONTAINER_PORT = '8000'
        PYTHON_EXE = 'C:\\Users\\india\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON_EXE%" -m pip install --upgrade pip'
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
            }
        }

        stage('Django Check') {
            steps {
                bat '"%PYTHON_EXE%" manage.py check'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %APP_NAME%:latest -t %APP_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker rm -f %CONTAINER_NAME% || exit /b 0'
                bat 'docker run -d --name %CONTAINER_NAME% -p %HOST_PORT%:%CONTAINER_PORT% %APP_NAME%:latest'
            }
        }
    }

    post {
        success {
            echo 'Build and deployment completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check Jenkins console output.'
        }
    }
}
