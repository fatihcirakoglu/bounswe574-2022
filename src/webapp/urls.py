from django.urls import path
from webapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("webapp/<name>", views.hello_there, name="hello_there")
]