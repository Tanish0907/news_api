from django.shortcuts import render
from django.http import JsonResponse
from scraper import News

def aajtak(request):
    a=News()
    return JsonResponse(a.scrape_aaj_tak())
# Create your views here.
