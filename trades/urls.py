from django.conf.urls import patterns, include, url
from trades import views

urlpatterns = patterns('',
        url(r'^$', views.index, name="index"),
	url(r'^trade/cancel/(?P<trade_id>\d+)/$', views.trade_cancel, name="trade_cancel"),
	url(r'^trade/accept/(?P<trade_id>\d+)/$', views.trade_accept, name="trade_accept"),
)

