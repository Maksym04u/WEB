from django.http import JsonResponse
from .test import test_task

def trigger_test_task(request):
    test_task.delay()
    return JsonResponse({"message": "Task triggered!"})