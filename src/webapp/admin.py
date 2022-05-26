from django.contrib import admin
from .models import Course, FavouriteCourse, Post, FavouritePost, Profile, Comment, TagDict

# Register your models here.
admin.site.register(Course)
admin.site.register(FavouriteCourse)
admin.site.register(Post)
admin.site.register(FavouritePost)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(TagDict)