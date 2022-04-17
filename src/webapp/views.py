from django.utils.timezone import datetime
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from webapp.forms import CustomUserCreationForm


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

def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
