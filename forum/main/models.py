from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

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
        return "/forum/%s" % self.id

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
        return "/topic/%s" % self.id

class Post(models.Model):
    forum = models.ForeignKey('Forum')
    topic = models.ForeignKey('Topic')
    user = models.ForeignKey(User)
    ip = models.GenericIPAddressField()
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    def formatted_content(self):
        formatted_content = self.content
        #$text = preg_replace("/\[quote:$uid=\"(.*?)\"\]/si", $bbcode_tpl['quote_username_open'], $text);
        # quotes
        #r = re.compile(r"/\[quote:\w\]/")
        #formatted_content = r.sub(r'<blockquote>', formatted_content)
        #r = re.compile(r"\[/quote:\w\]")
        #formatted_content = r.sub(r'</blockquote>', formatted_content)
        # links
        #r = re.compile(r"(http://[^ ]+)")
        #formatted_content = r.sub(r'<a href="\1" rel="nofollow" target="_blank">\1</a>', formatted_content)
        # breaks
        formatted_content = formatted_content.replace('\n', '<br />')
        return formatted_content


#class Profile(models.Model):
#    user = AutoOneToOneField(User)