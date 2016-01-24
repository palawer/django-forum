from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users$', views.users_view, name='users_view'),
    url(r'^search$', views.search_view, name='search_view'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^forum/(?P<slug>[a-zA-Z0-9-]+)$', views.forum_view, name='forum_view'),
    url(r'^topic/(?P<slug>[a-zA-Z0-9-._]+)$', views.topic_view, name='topic_view'),
    url(r'^post/(?P<post_id>[0-9]+)$', views.post_view, name='post_view'),
    url(r'^user/(?P<username>[a-zA-Z0-9-._]+)/posts$', views.profile_posts, name='profile_posts'),
    url(r'^user/(?P<username>[a-zA-Z0-9-._]+)$', views.profile_view, name='profile_view'),
]
