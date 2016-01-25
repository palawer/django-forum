from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from forum import settings
from .utils import *
import urllib, hashlib, os.path

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

class Forum(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    topics = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    order = models.IntegerField(default=0)
    last_post = models.ForeignKey('Post',  related_name='last_forum_post', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
    def url(self):
        return "/forum/%s" % self.slug

class Topic(models.Model):
    user = models.ForeignKey(User)
    forum = models.ForeignKey('Forum')
    title = models.CharField(max_length=250)
    first_post = models.ForeignKey('Post', related_name='first_topic_post')
    last_post = models.ForeignKey('Post', related_name='last_topic_post')
    views = models.PositiveIntegerField(default=0)
    replies = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)
    
    def url(self):
        return "/topic/%s" % self.slug

class Post(models.Model):
    forum = models.ForeignKey('Forum')
    topic = models.ForeignKey('Topic')
    user = models.ForeignKey(User)
    ip = models.GenericIPAddressField()
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    def url(self):
        return "/post/%s" % self.id
    
    def formatted_content(self):
        formatted_content = self.content
        formatted_content = bbcode(formatted_content)
        formatted_content = emojis(formatted_content)
        formatted_content = formatted_content.replace('\n', '<br />')
        return formatted_content

class Profile(models.Model):
    user = models.OneToOneField(User)
    posts = models.PositiveIntegerField(default=0)
    timezone = models.FloatField(default=0)
    avatar = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    website = models.URLField(max_length=200)
    location = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.user.username
    
    def url(self):
        return "/user/%s" % self.user.username
    
    def avatar_url(self):
        if self.avatar:
            file_path = "/static/img/avatars/%s" % self.avatar
            return file_path
            #if os.path.exists(file_path):
            #    return "/" + file_path
        
        # gravatar
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.user.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':'retro', 's':str(100)}) # identicon
        return gravatar_url

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
