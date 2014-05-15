from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from waivers import views

urlpatterns = patterns('',
        url(r'^$', views.index, name="index"),
	url(r'^waivers/cancel/(?P<waiver_id>\d+)/$', views.waiver_cancel, name="waiver_cancel"),
	url(r'^waivers/add/$', views.waiver_add, name="waiver_add"),
)

