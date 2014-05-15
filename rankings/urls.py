from django.conf.urls import patters, include, url

from rankings import views

urlpatters = patters('',
	url(r'^$', views.index, name="index"),
	url(r'^week/(?P<rankings_week>\d+)/', views.rankings_week, name="rankings_week"),
)
