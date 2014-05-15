from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from hockeypool import views

urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),
	url(r'^ajax/', include('ajax.urls')),
	url(r'^forum/', include('forum.urls')),
	url(r'^draft/', include('draft.urls')),
	url(r'^match/', include('match.urls')),
	url(r'^waivers/' include('waivers.urls')),
	url(r'^trades/', include('trades.urls')),
	url(r'^rankings/', include('rankings.urls')),

	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', views.logout_page, name="logout_page"),
	url(r'^profile/$', views.profile_index, name="profile_index"),
	url(r'^register/$', views.register, name="register"),
	url(r'^skater/(?P<skater_id>\d+)/$', views.skater_detail, name="skater_detail"),
	url(r'^skater/injury/(?P<skater_id>\d+)/$', views.injury_detail, name="injury_detail"),
	url(r'^skater/injury/$', views.injury_index, name="injury_index"),
	url(r'^skater/freeagents/$', views.freeagents_index, name="freeagents"),
	url(r'^skater/freeagents2/$', views.freeagents_index2, name="freeagents2"),
	url(r'^skater/$', views.skater_index, name="skater_index"),
	url(r'^standings/$', views.standings_index, name="standings_index"),
	url(r'^standings/east/$', views.standings_east, name="standings_east"),
	url(r'^standings/west/$', views.standings_west, name="standings_west"),
	url(r'^team/(?P<team_id>\d+)/$', views.team_detail, name="team_detail"),
	url(r'^team/$', views.team_index, name="team_index"),
	url(r'^$', views.index, name='index')
)
