from django.urls import path
from .views import github_webhook
from .views import download_resume, hello_devops, home


urlpatterns = [
    path("", home, name="home"),
    path("hello", hello_devops, name="hello-devops"),
    path("hello/", hello_devops, name="hello-devops-slash"),
    path("resume/", download_resume, name="resume"),
    path("webhook/", github_webhook)
]
