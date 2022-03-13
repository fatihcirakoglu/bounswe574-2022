from django.shortcuts import render
import re
from django.utils.timezone import datetime
from django.http import HttpResponse


#def home(request):
#    return HttpResponse("Hello, this is initial page of Swe573 Django project!")

def home(request):
    return render(request, "webapp/home.html")

def about(request):
    return render(request, "webapp/about.html")

def hello_there(request, name):
    return render(
        request,
        'webapp/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )