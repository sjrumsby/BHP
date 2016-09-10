from django.conf.urls  import url, include
from ajax import views

urlpatterns = [
	url(r'^getPlayer$', views.getPlayer, name="getPlayer"),
	url(r'^skater/(?P<nhlID>[0-9]+)/$', views.getSkater, name="getSkater"),
	url(r'^player/(?P<playerID>[0-9]+)/$', views.getPlayerPopup, name="getPlayerPopup"),
	url(r'^getWaiverPlayer/(?P<player_name>[a-zA-Z ]*)/$', views.getWaiverPlayer, name="getWaiverPlayer"),
	url(r'^getTradeOwn/(?P<player_name>[a-zA-Z ]*)/$', views.getTradeOwn, name="getTradeOwn"),
	url(r'^getTradeOther/(?P<player_name>[a-zA-Z ]*)/$', views.getTradeOther, name="getTradeOther"),
	url(r'^draftUpdate$', views.draftUpdate, name="draftUpdate"),
	url(r'^pickPlayer$', views.pick_player, name="pick_player"),
	url(r'^updateStatus$', views.updateStatus, name="updateSatus"),
	url(r'^activateRoster$', views.activateRoster, name="activateRoster"),
	url(r'^tradePlayers$', views.tradePlayer, name="tradePlayer"),
	url(r'^updateTheme$', views.updateTheme, name="updateTheme"),
	url(r'^changePassword$', views.changePassword, name="changePassword"),
	url(r'^updateTeamName$', views.updateTeamName, name="updateTeamName"),
	url(r'^updateUsername$', views.updateUsername, name="updateUsername"),
]

