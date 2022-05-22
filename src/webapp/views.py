from operator import contains
from django.utils.timezone import datetime
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from webapp.forms import CustomUserCreationForm
from django.shortcuts import render,get_object_or_404
from .models import  Post
from django.db.models import Q


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


def post_list(request):

    post = Post.objects.all()

    return render(request, 'webapp/post_list.html', {'post': post })

def post_detail(request,id):

    post = get_object_or_404(Post, id=id)

    types = Post.objects.all()

    t = types.get(id=post.body.id)

    return render(request, 'webapp/post_detail.html', {'post': post, 'type': t.categories})

def search(request):
    query = request.GET.get('query', None)
    allposts=Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    params={'post_list':allposts,}
    return render(request,'search.html',params)