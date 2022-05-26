from . import views
from django.urls import path
from .views import CourseLikeToggle,CourseLikeAPIToggle,PostLikeToggle,PostLikeAPIToggle,ProfileUpdateView,ProfileView,PostUpdateView, CourseUpdateView
from django.urls import include, re_path as url

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    url(r"^accounts/login/$", views.loginUser, name="login"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('favorites/', views.favorites, name='favorites'),
    path('', views.courselist, name='home'),
    path('blog/create', views.PostCreateView.as_view(), name='create_blog'),
    path('course/create', views.CourseCreateView.as_view(), name='create_course'),
    path('post/like/<slug:slug>/', PostLikeToggle.as_view(), name='post-like-toggle'),
    path('postapi/like/<slug:slug>/', PostLikeAPIToggle.as_view(), name='post-like-api-toggle'),
    path('course/like/<slug:slug>/', CourseLikeToggle.as_view(), name='course-like-toggle'),
    path('courseapi/like/<slug:slug>/', CourseLikeAPIToggle.as_view(), name='course-like-api-toggle'),
    path('postdetail/<slug:slug>/', views.postdetail, name='post_detail'),
    path('coursedetail/<slug:slug>/', views.coursedetail, name='course_detail'),
    path('coursedetail/<slug:slug>/Favourites', views.Favorites, name='Favorites'),
    path('postdetail/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('coursedetail/<slug:slug>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('fetch_post', views.fetch_post, name="fetch_post"),
    path('fetch_course', views.fetch_course, name="fetch_course"),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/',views.about,name='about'),
    path('faq/',views.faq,name='faq'),
    path('search/',views.search,name='search'),
    path('posttags/<slug:slug>/', views.posts_by_tag, name='posts_by_tag'),
    path('coursetags/<slug:slug>/', views.courses_by_tag, name='courses_by_tag'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT)
