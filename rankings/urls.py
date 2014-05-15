from django.conf.urls import patterns, include, url

from rankings import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^week/(?P<rankings_week>\d+)/', views.rankings_week, name="rankings_week"),
)
