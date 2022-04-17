from os import path
from django.urls import include, re_path as url
from django.contrib.auth import views as auth_views
from webapp import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^home/", views.home, name='home'),
    url(r"^accounts/register/$", views.register, name="register"),
]