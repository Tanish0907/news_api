from django.shortcuts import render
from django.http import JsonResponse

def test(request):
    return JsonResponse({"test":"abc"})
# Create your views here.
