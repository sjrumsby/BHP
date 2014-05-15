from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from forum import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^(?P<forum_id>\d+)/$', views.forum_detail, name="forum_detail"),
	url(r'^newthread/(?P<forum_id>\d+)/$', views.forum_newthread, name="forum_newthread"),
	url(r'^thread/(?P<thread_id>\d+)/$', views.forum_thread, name="forum_thread"),
	url(r'thread/(?P<thread_id>\d+)/reply/$', views.forum_thread_reply, name="forum_thread_reply"),
)

