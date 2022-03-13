from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is initial page of Swe573 Django project!")
