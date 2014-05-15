from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from draft import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^round/(?P<draft_round>\d+)/$', views.draft_round, name="draft_round"),
)

