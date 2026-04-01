# Full DevOps CI/CD Pipeline (Beginner Friendly)

This project gives you a simple Django app plus the core DevOps pieces around it:

- Git for version control
- Jenkins for CI/CD
- Docker for containerization
- Kubernetes for deployment and scaling
- Terraform for infrastructure provisioning
- Ansible for server setup

## 1. Project Structure

```text
.
|-- ansible/
|   |-- inventory.ini
|   `-- playbook.yml
|-- devops_project/
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|   `-- asgi.py
|-- hello/
|   |-- urls.py
|   `-- views.py
|-- k8s/
|   |-- deployment.yaml
|   `-- service.yaml
|-- terraform/
|   |-- main.tf
|   |-- outputs.tf
|   |-- terraform.tfvars.example
|   |-- variables.tf
|   `-- versions.tf
|-- .dockerignore
|-- .gitignore
|-- Dockerfile
|-- Jenkinsfile
|-- manage.py
|-- README.md
`-- requirements.txt
```

## 2. App Details

The Django app exposes one endpoint:

- `GET /hello`
- Response:

```json
{
  "message": "Hello DevOps"
}
```

## 3. Run Locally

### Quick start on Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-local.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\run-local.ps1
```

Open:

- `http://127.0.0.1:8000/hello`

### Manual start

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py runserver
```

## 4. Git Setup

```powershell
git init
git add .
git commit -m "Initial DevOps project"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## 5. Docker Setup

Docker is required on the machine where you want to build and run the container.

### Build image

```powershell
docker build -t devops-django-app .
```

### Run container

```powershell
docker run -d -p 8000:8000 --name devops-django-app devops-django-app
```

### Test

Open:

- `http://localhost:8000/hello`

## 6. Jenkins Pipeline

The `Jenkinsfile` is now parameterized and does the following:

1. Checks out code
2. Creates Python virtual environment
3. Runs `python manage.py check`
4. Builds Docker image
5. Pushes image to Docker Hub
6. Optionally runs the container on the Jenkins agent
7. Optionally deploys latest image to Kubernetes

### Jenkins prerequisites

- Jenkins agent should have `python3`
- Docker installed on Jenkins agent
- If using Kubernetes deployment, `kubectl` should also be installed
- Jenkins should have Docker Hub credentials stored as `Username with password`

### Jenkins plugins

- Pipeline
- Git
- GitHub Integration
- Credentials Binding
- Docker Pipeline

### Jenkins parameters

- `DOCKERHUB_REPO`: example `yourname/devops-django-app`
- `DOCKER_CREDENTIALS_ID`: example `dockerhub-creds`
- `KUBE_NAMESPACE`: default `devops-demo`
- `DEPLOY_TO_K8S`: set `true` to deploy
- `RUN_LOCAL_CONTAINER`: set `true` only if Jenkins agent itself should run the app

### Example Jenkins job flow

- Create a Pipeline job in Jenkins
- Point it to your GitHub repository
- Use `Jenkinsfile` from repo
- Add Docker Hub credentials in Jenkins Credentials
- Trigger build manually or through GitHub webhook

### Recommended Jenkins credentials

- Kind: `Username with password`
- ID: `dockerhub-creds`
- Username: your Docker Hub username
- Password: your Docker Hub password or access token

### Recommended webhook flow

- GitHub repo `Settings > Webhooks`
- Payload URL: `http://<your-jenkins-server>:8080/github-webhook/`
- Content type: `application/json`
- Event: `Just the push event`

## 7. Kubernetes Deployment

Kubernetes files are in `k8s/`.

Before applying:

- The Jenkins pipeline injects the image name automatically during deploy
- Default namespace is `devops-demo`
- Make sure your cluster can pull your Docker Hub image

Apply manifests:

```bash
sed "s|NAMESPACE_PLACEHOLDER|devops-demo|g" k8s/namespace.yaml | kubectl apply -f -
sed "s|NAMESPACE_PLACEHOLDER|devops-demo|g" k8s/service.yaml | kubectl apply -f -
sed "s|IMAGE_PLACEHOLDER|yourname/devops-django-app:latest|g; s|NAMESPACE_PLACEHOLDER|devops-demo|g" k8s/deployment.yaml | kubectl apply -f -
kubectl get pods
kubectl get svc
```

The service exposes app on port `30080`.

## 8. Terraform Infrastructure

Terraform files create:

- One EC2 instance
- One security group with ports:
  - `22` for SSH
  - `80` for web
  - `8080` for Jenkins
  - `30080` for Kubernetes NodePort

### Steps

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

Before `terraform apply`, edit `terraform.tfvars` with:

- valid `ami_id`
- your `key_name`
- your preferred `allowed_ssh_cidr`

## 9. Ansible Server Setup

Update `ansible/inventory.ini` with:

- your server public IP
- correct SSH key path

Then run:

```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml
```

This playbook:

- updates apt cache
- installs Docker
- installs `kubectl`
- starts Docker service

## 10. Suggested End-to-End Flow

1. Push code to GitHub
2. Jenkins pulls latest code
3. Jenkins builds Docker image
4. Jenkins pushes image to Docker Hub
5. Jenkins updates Kubernetes deployment with the latest image
6. Terraform creates server
7. Ansible configures server tools

## 11. Important Notes

- Terraform AMI is intentionally variable-based, so you can use the correct AMI for your AWS region
- Jenkins shell steps assume a Linux-based Jenkins agent
- If you use Jenkins on Windows, the `sh` steps should be converted to `bat` or `powershell`
- `k8s/deployment.yaml` intentionally uses placeholders because Jenkins replaces them at deploy time
- Docker is not installed in this workspace right now, so container build/run must be done on a Docker-enabled machine

## 12. Next Improvements

- Add Docker Hub push stage in Jenkins
- Add GitHub webhook integration
- Add ingress for Kubernetes
- Add Helm chart
- Add Jenkins credentials for Docker Hub and kubeconfig
