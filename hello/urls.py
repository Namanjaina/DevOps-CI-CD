from django.urls import path
from .views import github_webhook, download_resume, hello_devops, home

urlpatterns = [
    path("", home, name="home"),
    path("hello/", hello_devops, name="hello-devops"),
    path("resume/", download_resume, name="resume"),
    path("webhook/", github_webhook, name="github-webhook"),
]