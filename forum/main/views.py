from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *

TOPICS_PER_PAGE = 20
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



def topic_view(request, topic_id):
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

def topic_slug(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    return topic_view(request, topic.id)

def post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {
        'post': post,
    })

def profile_view(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    
    return render(request, 'profile.html', {
        'profile': profile,
    })

def profile_topics(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    
    topics_list = Topic.objects.filter(user=user_id).order_by('-id')
    
    paginator = Paginator(topics_list, TOPICS_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    
    return render(request, 'profile_topics.html', {
        'profile': profile,
        'topics': topics,
    })

def profile_posts(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    
    posts_list = Post.objects.filter(user=user_id).order_by('-id')
    
    paginator = Paginator(posts_list, POSTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'profile_posts.html', {
        'profile': profile,
        'posts': posts,
    })




