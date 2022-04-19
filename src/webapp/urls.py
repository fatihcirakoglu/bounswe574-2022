from os import path
from django.urls import include, re_path as url
from django.contrib.auth import views as auth_views
from webapp import views
from django.urls import path

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^home/", views.home, name='home'),
    url(r"^accounts/register/$", views.register, name="register"),
    url(r"^post_list/$", views.post_list, name='post_list'),
    url(r"^post_detail/$", views.post_detail, name='post_detail'),
    url(r"^search/$", views.search, name='search'),
]