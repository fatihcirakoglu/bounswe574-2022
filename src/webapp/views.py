from django.shortcuts import render
import re
from django.utils.timezone import datetime
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, this is initial page of Swe573 Django project!")

def hello_there(request, name):
    return render(
        request,
        'webapp/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )