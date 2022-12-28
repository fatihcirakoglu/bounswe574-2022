from django.shortcuts import render, redirect
from django.views import generic
from .models import Course, Post, FavouriteCourse, FavouritePost, Profile, Comment, EntityManager
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.views.generic import RedirectView,TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render,get_object_or_404
import json
from django.forms import model_to_dict
from .forms import SignupForm, UserForm,ProfileForm, CommentForm
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from taggit.models import Tag
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import datetime
from .utils import get_qcode_keywords


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    return str(o)

def loginUser(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
        return render(request, "login.html")
    return redirect("home")


def logoutUser(request):
    logout(request)
    messages.info(request, "Logged out of LetsColearn")
    return redirect("home")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_c = request.POST.get("password-c")
        if (password == password_c):
            try:
                user = User.objects.create_user(username, email, password);
                user.save()
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect("home")
            except IntegrityError:
                messages.info(request, "Try different Username")
                return render(request, "signup.html")
        messages.error(request, "Password doesn't match Confirm Password")
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "signup.html")


def postlist(request):
    
    post_list= Paginator(Post.objects.all().order_by('-created_on'),2)
    page= request.GET.get('page')

    try:
         posts = post_list.page(page)
    except PageNotAnInteger:
         posts = post_list.page(1)
    except EmptyPage:
         posts = post_list.page(post_list.num_pages)

    return render(request,'index.html', {"post_list": posts})


def courselist(request):
    
    course_list= Paginator(Course.objects.all().order_by('-created_on'),2)
    page= request.GET.get('page')

    try:
         courses = course_list.page(page)
    except PageNotAnInteger:
         courses = course_list.page(1)
    except EmptyPage:
         courses = course_list.page(course_list.num_pages)

    return render(request,'index.html', {"course_list": courses})

def fetch_course(request):
    course_list= Paginator(Course.objects.all().order_by('-created_on'),2)
    page=request.POST.get("page")

    try:
        courses = course_list.page(page)
    except PageNotAnInteger:
        courses = course_list.page(1)
    except EmptyPage:
        courses = course_list.page(course_list.num_pages)

    course_dic = {
        "number": courses.number,
        "has_next": courses.has_next(),
        "has_previous": courses.has_previous(),
        "courses": []
    }

    for i in course_list.page(page):
        course_dic["courses"].append(i.__dict__)
    
    for i in course_dic["courses"]:
        i["author"]=User.objects.get(id = i.get("author_id")).username

   
    return JsonResponse({"course_list": json.dumps(course_dic, default = default)})


def fetch_post(request):
    post_list= Paginator(Post.objects.all().order_by('-created_on'),2)
    page=request.POST.get("page")

    try:
        posts = post_list.page(page)
    except PageNotAnInteger:
        posts = post_list.page(1)
    except EmptyPage:
        posts = post_list.page(post_list.num_pages)

    post_dic = {
        "number": posts.number,
        "has_next": posts.has_next(),
        "has_previous": posts.has_previous(),
        "posts": []
    }

    for i in post_list.page(page):
        post_dic["posts"].append(i.__dict__)
    
    for i in post_dic["posts"]:
        i["author"]=User.objects.get(id = i.get("author_id")).username

   
    return JsonResponse({"post_list": json.dumps(post_dic, default = default)})

def postdetail(request, slug):
        
    post = Post.objects.get(slug=slug)
    comments=Comment.objects.filter(post=post, parent__isnull=True).order_by('-id')
    post.read_count += 1
    post.save()


    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST or None)
        if comment_form.is_valid():
            #comment = Comment.objects.create(post=post, name=name, body=body)
            #comment.save()
            parent_obj = None
            body = request.POST.get('body')
            name = request.POST.get('name')
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            #comment = Comment.objects.create(post=post, name=name, body=body)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    return render(request, 'postdetail.html', {'post': post,
                                   'comments' : comments, 'comment_form' : comment_form})

def coursedetail(request, slug):
        
    course = Course.objects.get(slug=slug)
    posts = Post.objects.filter(course_id=course.id).order_by('-id')
    course.read_count += 1
    course.save()

    if request.user.is_authenticated:
        Favourites,_ = FavouriteCourse.objects.get_or_create(user=request.user)
    course_in_favorites = None

    if request.user.is_authenticated:
        if course in Favourites.courses.all():
            course_in_favorites = True
        else:
            course_in_favorites = False

    FavouritesUsers=FavouriteCourse.objects.filter(Q(courses=course.id) | Q(courses=course.id))

    return render(request, 'coursedetail.html', {'course': course, 'course_in_favorites': course_in_favorites,'posts' : posts,"FavouritesUsers":FavouritesUsers})

def Favorites(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    Favourites,_ = FavouriteCourse.objects.get_or_create(user=request.user)
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        course = None

    if course not in Favourites.courses.all():
        Favourites.courses.add(course)
    else:
        Favourites.courses.remove(course)
    
    Favourites.save()
    
    return HttpResponse('Success')


def favorites(request):
    user = request.user
    FavCourses,_ = FavouriteCourse.objects.get_or_create(user=user)
    usercourses=Course.objects.filter(Q(author=user) | Q(author=user))
    course_list = FavCourses.courses.all()
    all_courses = Course.objects.all().order_by('-created_on')
    user_courses = (usercourses | course_list).distinct()
    user_keywords = []
    user_course_slug_list = []

    for course in user_courses:
        user_course_slug_list.append(course.slug)
        user_keywords += course.related_qcodes

    recommended_courses = []

    for course in all_courses:
        if course.slug not in user_course_slug_list:
            keywords = course.related_qcodes
            matches = list(set(user_keywords).intersection(set(keywords)))
            if len(matches) > 0:
                recommended_courses.append(course)
    return render(request, 'favourites.html', { 'course_list': course_list, "favorites": True,"usercourses":usercourses, 'recommended_courses': recommended_courses})


def about(request):
    context={}
    return render(request,'about.html',context=context)

def faq(request):
    context={}
    return render(request,'faq.html',context=context)

def search(request):
    query = request.GET.get('query', None)
    allcourses=Course.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    params={'course_list':allcourses,}
    return render(request,'search.html',params)


class PostLikeToggle(RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        id_ = self.kwargs.get("slug")
        obj = get_object_or_404(Post,slug=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                 obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

class CourseLikeToggle(RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        id_ = self.kwargs.get("slug")
        obj = get_object_or_404(Course,slug=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                 obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None,format=None):
        obj = get_object_or_404(Post,slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        verb = None
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                verb = 'Like'
                obj.likes.remove(user)
                count = obj.likes.all().count()
            else:
                liked = True
                verb = 'Unlike'
                obj.likes.add(user)
                count = obj.likes.all().count()
            updated = True
        data = {
            "updated":updated,
            "liked":liked,
            "count":count,
            "verb":verb
        }
        return Response(data)

class CourseLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None,format=None):
        obj = get_object_or_404(Course,slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        verb = None
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                verb = 'Like'
                obj.likes.remove(user)
                count = obj.likes.all().count()
            else:
                liked = True
                verb = 'Unlike'
                obj.likes.add(user)
                count = obj.likes.all().count()
            updated = True
        data = {
            "updated":updated,
            "liked":liked,
            "count":count,
            "verb":verb
        }
        return Response(data)


from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile

from django.contrib import messages

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm()
    profile_form = ProfileForm()
    template_name = 'profile-update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)




class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content','image','tags']

    template_name ='post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'content','image','tags']

    template_name ='course_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def posts_by_tag(request, slug):
    tags = Tag.objects.filter(slug=slug).values_list('name', flat=True)
    posts = Post.objects.filter(tags__name__in=tags)

    return render(request, 'postsbytag.html', { 'posts': posts,'tags':tags.first})

def courses_by_tag(request, slug):
    tags = Tag.objects.filter(slug=slug).values_list('name', flat=True)
    courses = Course.objects.filter(tags__name__in=tags)

    return render(request, 'coursesbytag.html', { 'courses': courses,'tags':tags.first})


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['course', 'title', 'content', 'image', 'tags']
    template_name = 'post_form.html'
    redirect_field_name = "redirect"  # added
    redirect_authenticated_user = True  # added

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CourseCreateView(LoginRequiredMixin,CreateView):
    model = Course
    fields = ['entity_wikidata', 'title', 'content', 'image', 'tags']
    template_name = 'course_form.html'
    redirect_field_name = "redirect"  # added
    redirect_authenticated_user = True  # added

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def CourseCreateStart(request):
    if request.method == 'POST':
        tagkeyword = request.POST.get("tagkeyword")
        if (tagkeyword):
            EntityManager.run(tagkeyword)
            return redirect('create_course')
        return redirect('course_create_start')
    return render(request, "course_create_start.html")