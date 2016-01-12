from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *

TOPICS_PER_PAGE = 25
POSTS_PER_PAGE = 10

def index(request):
    topics_list = Topic.objects.exclude(forum=5).exclude(forum=6).order_by('-last_post')
    forums = Forum.objects.all().order_by('category__order', 'order')
    
    paginator = Paginator(topics_list, TOPICS_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    
    return render(request, 'index.html', {
        'topics': topics,
        'forums': forums,
    })

def forum(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    topics_list = Topic.objects.filter(forum=forum_id).order_by('-last_post')
    
    paginator = Paginator(topics_list, TOPICS_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    
    return render(request, 'forum.html', {
        'forum': forum,
        'topics': topics,
    })

def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    posts_list = Post.objects.filter(topic=topic)
    
    paginator = Paginator(posts_list, POSTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'topic.html', {
        'topic': topic,
        'posts': posts,
    })

def profile(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    
    return render(request, 'profile.html', {
        'profile': profile,
    })






