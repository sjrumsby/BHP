from django.conf.urls import patterns, url

from match import views

urlpatterns = patterns('',
	url(r'^match/(?P<match_id>\d+)/$', views.match_detail, name="match_detail"),
	url(r'^match/week/(?P<match_week>\d+)/$', views.match_week, name="match_week"),
	url(r'^match/activate/$', views.match_activate, name="match_activate"),
	url(r'^match/$', views.match_index, name="match_index"),
)
