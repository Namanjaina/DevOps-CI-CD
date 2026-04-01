from django.http import JsonResponse


def hello_devops(request):
    return JsonResponse({"message": "Hello DevOps"})

