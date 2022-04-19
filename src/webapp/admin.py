from django.contrib import admin

# Register your models here.

from .models import Category, Post, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ("title",)

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author",)

admin.site.register(Comment, CommentAdmin)