from pathlib import Path

from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import render


def hello_devops(request):
    return JsonResponse({"message": "Hello DevOps"})


def download_resume(request):
    resume_path = Path(settings.BASE_DIR) / "hello" / "static" / "hello" / "aman-kumar-resume.txt"
    return FileResponse(resume_path.open("rb"), as_attachment=True, filename="aman-kumar-resume.txt")


def home(request):
    profile = {
        "name": "Naman jain",
        "role": "DevOps Engineer and Web Developer",
        "bio": "I build fast web experiences and deployment pipelines that are clean, reliable, and ready for real-world delivery.",
        "location": "India",
        "email": "aman.dev@example.com",
        "availability": "Available for freelance and full-time roles",
    }

    projects = [
        {
            "tag": "Featured Build",
            "title": "DevOps Automation Platform",
            "description": "A deployment-focused Django project wired with Jenkins, Docker, Kubernetes, Terraform, and Ansible.",
            "impact": "Reduced manual deployment steps by turning infra and release flow into a repeatable pipeline.",
        },
        {
            "tag": "System Design",
            "title": "Release Flow Architecture",
            "description": "From local development to container image delivery, the stack is laid out to show a practical CI/CD path.",
            "impact": "Improved visibility of each stage from commit to rollout using a portfolio-ready project structure.",
        },
        {
            "tag": "Ops Toolkit",
            "title": "Infrastructure as Code",
            "description": "Reusable provisioning and configuration files make the environment easier to recreate and scale.",
            "impact": "Made environment setup faster and easier to reproduce across teams and machines.",
        },
    ]

    stack = [
        "Django",
        "Python",
        "Jenkins",
        "Docker",
        "Kubernetes",
        "Terraform",
        "Ansible",
        "Git",
    ]

    services = [
        "Portfolio websites and landing pages",
        "Django backend setup and API delivery",
        "Docker and Jenkins based CI/CD pipelines",
        "Kubernetes deployment structure",
    ]

    stats = [
        {"value": "01", "label": "Full-stack demo website"},
        {"value": "05", "label": "Deployment layers covered"},
        {"value": "24/7", "label": "Built for repeatable delivery"},
    ]

    timeline = [
        {
            "period": "Phase 01",
            "title": "Design the application surface",
            "description": "Create a web entry point that looks polished and remains compatible with the existing Django app.",
        },
        {
            "period": "Phase 02",
            "title": "Connect CI/CD workflow",
            "description": "Use Jenkins, Docker, and Kubernetes files from the repo to move the project toward automated deployment.",
        },
        {
            "period": "Phase 03",
            "title": "Provision infra cleanly",
            "description": "Terraform and Ansible provide the repeatable infrastructure layer behind the application delivery pipeline.",
        },
    ]

    experience = [
        {
            "period": "2025 - Present",
            "title": "DevOps and Backend Projects",
            "description": "Worked on CI/CD demos, deployment workflows, and Python web applications focused on practical automation.",
        },
        {
            "period": "2024 - 2025",
            "title": "Frontend and Portfolio Builds",
            "description": "Designed responsive interfaces, developer landing pages, and showcase websites with clean section-driven layouts.",
        },
    ]

    social_links = [
        {"label": "GitHub", "url": "https://github.com/yourusername"},
        {"label": "LinkedIn", "url": "https://www.linkedin.com/in/yourusername"},
        {"label": "Email", "url": "mailto:aman.dev@example.com"},
    ]

    contact_points = [
        "Local preview at http://127.0.0.1:8000/",
        "API response available at /hello/",
        "Ready to extend into a real portfolio or project showcase",
    ]

    context = {
        "profile": profile,
        "projects": projects,
        "stack": stack,
        "services": services,
        "stats": stats,
        "timeline": timeline,
        "experience": experience,
        "social_links": social_links,
        "contact_points": contact_points,
        "api_url": "/hello/",
        "resume_url": "/resume/",
    }
    return render(request, "hello/index.html", context)
