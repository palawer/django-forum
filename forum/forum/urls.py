from django.conf.urls import include, url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users$', views.users_view, name='users_view'),
    url(r'^search$', views.search_view, name='search_view'),
    
    url(r'^forum/(?P<slug>[a-zA-Z0-9-]+)$', views.forum_view, name='forum_view'),
    
    url(r'^topic/(?P<topic_id>[0-9]+)$', views.topic_view, name='topic_view'),
    url(r'^topic/(?P<topic_slug>[a-zA-Z0-9-._]+)$', views.topic_slug, name='topic_slug'),
    
    url(r'^post/(?P<post_id>[0-9]+)$', views.post_view, name='post_view'),
    
    url(r'^user/(?P<user_id>[0-9]+)/topics$', views.profile_topics, name='profile_topics'),
    url(r'^user/(?P<user_id>[0-9]+)/posts$', views.profile_posts, name='profile_posts'),
    url(r'^user/(?P<user_id>[0-9]+)$', views.profile_view, name='profile_view'),
    
    #url(r'^admin/', include(admin.site.urls)),
]
