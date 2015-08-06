from django.conf.urls import patterns, url

from match import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^(?P<match_id>\d+)/$', views.match_detail, name="match_detail"),
	url(r'^week/(?P<match_week>\d+)/$', views.match_week, name="match_week"),
	url(r'^activate/$', views.match_activate, name="match_activate"),
)
