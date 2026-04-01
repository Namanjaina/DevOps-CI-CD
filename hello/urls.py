from django.urls import path

from .views import hello_devops


urlpatterns = [
    path("hello", hello_devops, name="hello-devops"),
    path("hello/", hello_devops, name="hello-devops-slash"),
]

