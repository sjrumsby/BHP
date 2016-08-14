from django.conf.urls  import url, include
from draft import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^round/(?P<draft_round>\d+)/$', views.draft_round, name="draft_round"),
]

