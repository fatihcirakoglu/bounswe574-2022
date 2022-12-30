from django.db import models
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from .utils import get_read_time, column_exists, get_qcode_keywords
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
from django.dispatch import receiver
from ckeditor.fields import RichTextField
import requests


# Create your models here.
class TagDict(models.Model):
    tag = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.tag


class WikidataFirstEntityDict(models.Model):
    entity_description = models.TextField()
    entity_qcode = models.CharField(max_length=20)
    entity_title = models.CharField(max_length=100)

    def __str__(self):
        return self.entity_title + " -> " + self.entity_description


class WikidataSecondEntityDict(models.Model):
    entity_description = models.TextField()
    entity_qcode = models.CharField(max_length=20)
    entity_title = models.CharField(max_length=100)

    def __str__(self):
        return self.entity_title + " -> " + self.entity_description


class WikidataThirdEntityDict(models.Model):
    entity_description = models.TextField()
    entity_qcode = models.CharField(max_length=20)
    entity_title = models.CharField(max_length=100)

    def __str__(self):
        return self.entity_title + " -> " + self.entity_description


class EntityManager:
    def flush():
        WikidataFirstEntityDict.objects.all().delete()
        WikidataSecondEntityDict.objects.all().delete()
        WikidataThirdEntityDict.objects.all().delete()

    def run(keywords:str):
        EntityManager.flush()
        keywords = keywords.split(",")
        EntityManager.save_entity_dict(keywords)

    def save_entity_dict(keywords:list):
        results = EntityManager.search_wikidata(keywords[0])
        for index in range(len(results)):
            if 'description' not in list(results[index].keys()) or 'label' not in list(results[index].keys()):
                continue
            WikidataFirstEntityDict.objects.get_or_create(
                entity_description = results[index]['description'], 
                entity_qcode = results[index]['id'],
                entity_title = results[index]['label']
            )
        if len(keywords) > 1:
            results = EntityManager.search_wikidata(keywords[1])
            for index in range(len(results)):
                if 'description' not in list(results[index].keys()) or 'label' not in list(results[index].keys()):
                    continue
                WikidataSecondEntityDict.objects.get_or_create(
                    entity_description = results[index]['description'], 
                    entity_qcode = results[index]['id'],
                    entity_title = results[index]['label']
                )
        if len(keywords) > 2:
            results = EntityManager.search_wikidata(keywords[2])
            for index in range(len(results)):
                if 'description' not in list(results[index].keys()) or 'label' not in list(results[index].keys()):
                    continue
                WikidataThirdEntityDict.objects.get_or_create(
                    entity_description = results[index]['description'], 
                    entity_qcode = results[index]['id'],
                    entity_title = results[index]['label']
                )
        
    def search_wikidata(keyword: str):
        API_ENDPOINT = "https://www.wikidata.org/w/api.php"
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': keyword,
            'limit': "max",
        }
        search_result = requests.get(API_ENDPOINT, params = params)
        return search_result.json()['search']


class Course(models.Model):
    CATEGORY_CHOICES = ( 
        ("1", "Programming/Technology"), 
        ("2", "Health/Fitness"), 
        ("3", "Personal"), 
        ("4", "Fashion"), 
        ("5", "Food"), 
        ("6", "Travel"), 
        ("7", "Business"), 
        ("8", "Art"),
        ("9", "Other"), 
    )   

    category = models.CharField( 
        max_length = 20, 
        choices = CATEGORY_CHOICES, 
        default = '1'
        )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    read_count = models.IntegerField(default=0, editable=False)
    read_time = models.IntegerField(default=0, editable=False)
    likes = models.ManyToManyField(User, blank=True, related_name='course_likes')
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tags = TaggableManager(blank=True)
    first_wikidata_entity = models.ForeignKey(WikidataFirstEntityDict, on_delete= models.SET_NULL, null=True, blank=True)
    second_wikidata_entity = models.ForeignKey(WikidataSecondEntityDict, on_delete= models.SET_NULL, null=True, blank=True)
    third_wikidata_entity = models.ForeignKey(WikidataThirdEntityDict, on_delete= models.SET_NULL, null=True, blank=True)
    first_qcode = models.CharField(default = ' ', max_length=20, editable= False)
    second_qcode = models.CharField(default = ' ', max_length=20, editable= False)
    third_qcode = models.CharField(default = ' ', max_length=20, editable= False)
    related_qcodes = ListCharField(default = [],
        base_field=models.CharField(max_length=20),
        size=45,
        max_length=(45 * 21)
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        if self.first_wikidata_entity:
            self.first_qcode = self.first_wikidata_entity.entity_qcode
            self.related_qcodes = get_qcode_keywords(self.first_qcode)
        if self.second_wikidata_entity:
            self.second_qcode = self.second_wikidata_entity.entity_qcode
            self.related_qcodes += get_qcode_keywords(self.second_qcode)
        if self.third_wikidata_entity:
            self.third_qcode = self.third_wikidata_entity.entity_qcode
            self.related_qcodes += get_qcode_keywords(self.third_qcode)
        super().save(*args, **kwargs)

        for tag in self.tags.all():
            tag_dict,_ = TagDict.objects.get_or_create(tag=str(tag))
            tag_dict.count += 1
            tag_dict.save()

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={"slug":self.slug})

    def get_like_url(self):
        return reverse('course-like-toggle', kwargs={"slug":self.slug})
    
    def get_api_like_url(self):
        return reverse('course-like-api-toggle', kwargs={"slug":self.slug})
        


def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        instance.read_time = get_read_time(instance.content)

pre_save.connect(pre_save_course_receiver, sender=Course)


class Post(models.Model):
    course = models.ForeignKey(Course,null=True,on_delete=models.CASCADE,related_name='posts')
    #category = course.get_attname()
    #course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    read_count = models.IntegerField(default=0, editable=False)
    read_time = models.IntegerField(default=0, editable=False)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

        for tag in self.tags.all():
            tag_dict,_ = TagDict.objects.get_or_create(tag=str(tag))
            tag_dict.count += 1
            tag_dict.save()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug":self.slug})

    def get_like_url(self):
        return reverse('post-like-toggle', kwargs={"slug":self.slug})
    
    def get_api_like_url(self):
        return reverse('post-like-api-toggle', kwargs={"slug":self.slug})


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        instance.read_time = get_read_time(instance.content)

pre_save.connect(pre_save_post_receiver, sender=Post)



class FavouriteCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

class FavouritePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    profile_image = models.ImageField(default='default.jpeg', upload_to ='profile_pics', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
