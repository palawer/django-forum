from django.conf.urls import include, url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^forum/(?P<forum_id>[0-9]+)$', views.forum, name='forum'),
    url(r'^topic/(?P<topic_id>[0-9]+)$', views.topic, name='topic'),
    url(r'^user/(?P<user_id>[0-9]+)$', views.profile, name='profile'),
    url(r'^admin/', include(admin.site.urls)),
]
