from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import *

TOPICS_PER_PAGE = 20
POSTS_PER_PAGE = 10

def index(request):
    topics_list = Topic.objects.exclude(forum=6).exclude(forum=18).order_by('-last_post')
    forums = Forum.objects.exclude(id=6).exclude(id=18).order_by('category__order', 'order')
    
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

def forum_view(request, slug):
    forum = get_object_or_404(Forum, slug=slug)
    if forum.id in [6, 18]:
        raise Http404
    
    topics_list = Topic.objects.filter(forum=forum.id).order_by('-last_post')
    best_topics = Topic.objects.filter(forum=forum.id).order_by('-replies')[:10]
    
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
        'best_topics': best_topics,
    })

def topic_view(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if topic.forum.id in [6, 18]:
        raise Http404
    
    posts_list = Post.objects.filter(topic=topic)
    topics = Topic.objects.filter(forum=topic.forum.id).order_by('-last_post')[:10]
    last_post = Post.objects.get(pk=topic.last_post.id)
    top_users = Post.objects.filter(topic=topic).values('user_id').annotate(dcount=Count('user_id')).order_by('-dcount')[:10]
    
    new_dict = []
    for tmp in top_users:
        new_dict.append({
            'user': get_object_or_404(User, pk=tmp.get('user_id')),
            'count': tmp.get('dcount'),
        })
    
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
        'topics': topics,
        'top_users': new_dict,
        'last_post': last_post,
    })

def post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.forum.id in [6, 18]:
        raise Http404
    
    num = Post.objects.filter(topic=post.topic).filter(id__lt=post.id).count()
    page = (num / POSTS_PER_PAGE) + 1
    
    if page > 1:
        url = "?page=" + str(page) + "#post-" + str(post.id)
    else:
        url = "#post-" + str(post.id)
    
    return render(request, 'post.html', {
        'post': post,
        'url': url,
    })

def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    return render(request, 'profile.html', {
        'profile': profile,
    })

def profile_topics(request, username):
    profile = get_object_or_404(User, username=username)
    topics_list = Topic.objects.exclude(forum=6).exclude(forum=18).filter(user=profile.id).order_by('-id')
    
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

def profile_posts(request, username):
    profile = get_object_or_404(User, username=username)
    posts_list = Post.objects.exclude(forum=6).exclude(forum=18).filter(user=profile.id).order_by('-id')
    
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

def users_view(request):
    users_list = User.objects.all()

    paginator = Paginator(users_list, 36)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'users.html', {
        'users': users
    })

def search_view(request):
    return render(request, 'search.html', {
        
    })
