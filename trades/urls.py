from django.conf.urls  import url, include
from trades import views

urlpatterns = [
        url(r'^$', views.index, name="index"),
	url(r'^cancel/(?P<trade_id>\d+)/$', views.trade_cancel, name="trade_cancel"),
	url(r'^accept/(?P<trade_id>\d+)/$', views.trade_accept, name="trade_accept"),
]

