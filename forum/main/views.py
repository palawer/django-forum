from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *

def index(request):
    topics = Topic.objects.order_by('-last_post')[:25]
    forums = Forum.objects.all().order_by('category__order', 'order')
    
    return render(request, 'index.html', {
        'topics': topics,
        'forums': forums,
    })

def forum(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    topics = Topic.objects.filter(forum=forum_id).order_by('-last_post')[:25]
    
    return render(request, 'forum.html', {
        'forum': forum,
        'topics': topics,
    })

def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    posts = Post.objects.filter(topic=topic)[:25]
    
    return render(request, 'topic.html', {
        'topic': topic,
        'posts': posts,
    })