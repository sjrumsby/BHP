from django.conf.urls import patterns, url

from ajax import views

urlpatterns = patterns('',
	url(r'^getPlayer/(?P<player_name>[a-zA-Z ]*)/$', views.getPlayer, name="getPlayer"),
	url(r'^getWaiverPlayer/(?P<player_name>[a-zA-Z ]*)/$', views.getWaiverPlayer, name="getWaiverPlayer"),
	url(r'^getTradeOwn/(?P<player_name>[a-zA-Z ]*)/$', views.getTradeOwn, name="getTradeOwn"),
	url(r'^getTradeOther/(?P<player_name>[a-zA-Z ]*)/$', views.getTradeOther, name="getTradeOther"),
	url(r'^draftUpdate$', views.draftUpdate, name="draftUpdate"),
	url(r'^pickPlayer$', views.pick_player, name="pick_player"),
	url(r'^updateStatus$', views.updateStatus, name="updateSatus"),
	url(r'^activateRoster$', views.activateRoster, name="activateRoster"),
	url(r'^tradePlayers$', views.tradePlayer, name="tradePlayer"),
)

