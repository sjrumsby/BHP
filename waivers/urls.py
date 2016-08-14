from django.conf.urls  import url, include
from waivers import views

urlpatterns = [
        url(r'^$', views.index, name="index"),
	url(r'^cancel/(?P<waiver_id>\d+)/$', views.waiver_cancel, name="waiver_cancel"),
	url(r'^add/$', views.waiver_add, name="waiver_add"),
]

