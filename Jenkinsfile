pipeline {
    agent any

    parameters {
        string(name: 'DOCKERHUB_REPO', defaultValue: 'your-dockerhub-username/devops-django-app', description: 'Docker Hub repository name')
        string(name: 'DOCKER_CREDENTIALS_ID', defaultValue: 'dockerhub-creds', description: 'Jenkins username/password credentials ID for Docker Hub')
        string(name: 'KUBE_NAMESPACE', defaultValue: 'devops-demo', description: 'Kubernetes namespace for deployment')
        booleanParam(name: 'DEPLOY_TO_K8S', defaultValue: true, description: 'Deploy latest image to Kubernetes')
        booleanParam(name: 'RUN_LOCAL_CONTAINER', defaultValue: false, description: 'Run the container on the Jenkins agent after build')
    }

    environment {
        APP_NAME = 'devops-django-app'
        CONTAINER_NAME = 'devops-django-container'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        IMAGE_NAME = "${params.DOCKERHUB_REPO}"
        FULL_IMAGE = "${params.DOCKERHUB_REPO}:${env.BUILD_NUMBER}"
        LATEST_IMAGE = "${params.DOCKERHUB_REPO}:latest"
    }

    options {
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
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Django Checks') {
            steps {
                sh '. venv/bin/activate && python manage.py check'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${FULL_IMAGE} -t ${LATEST_IMAGE} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: params.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin'
                    sh 'docker push ${FULL_IMAGE}'
                    sh 'docker push ${LATEST_IMAGE}'
                }
            }
        }

        stage('Run Container Locally') {
            when {
                expression { return params.RUN_LOCAL_CONTAINER }
            }
            steps {
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh 'docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${LATEST_IMAGE}'
            }
        }

        stage('Deploy To Kubernetes') {
            when {
                expression { return params.DEPLOY_TO_K8S }
            }
            steps {
                sh 'sed "s|NAMESPACE_PLACEHOLDER|${KUBE_NAMESPACE}|g" k8s/namespace.yaml | kubectl apply -f -'
                sh 'sed "s|NAMESPACE_PLACEHOLDER|${KUBE_NAMESPACE}|g" k8s/service.yaml | kubectl apply -f -'
                sh 'sed "s|IMAGE_PLACEHOLDER|${LATEST_IMAGE}|g; s|NAMESPACE_PLACEHOLDER|${KUBE_NAMESPACE}|g" k8s/deployment.yaml | kubectl apply -f -'
                sh 'kubectl rollout status deployment/${APP_NAME} -n ${KUBE_NAMESPACE} --timeout=120s'
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}
