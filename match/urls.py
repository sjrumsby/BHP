from django.conf.urls  import url, include

from match import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^(?P<match_id>\d+)/$', views.match_detail, name="match_detail"),
	url(r'^week/(?P<week_number>\d+)/$', views.match_week, name="match_week"),
	url(r'^activate/$', views.match_activate, name="match_activate"),
]
