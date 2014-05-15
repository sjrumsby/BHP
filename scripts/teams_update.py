#!/usr/bin/python

import django
from sys import path
from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc
import HTMLParser, grequests, urllib2, re

django_path = '/django/django_bhp/'
if django_path not in path:
        path.append(django_path)

from django_bhp import settings
from django.core.management import setup_environ
setup_environ(settings)

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

class NHLOvernightParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.table = 0
		self.rec = 0
		self.player_data = []
		self.player = []
		self.count = 0

	def handle_starttag(self, tag, attributes):
		if self.table:
			if tag == 'tr':
				self.rec = 1
		if tag == 'tbody':
			self.table = 1
		if self.count == 1:
			for name, value in attributes:
				if name=='href':
					id = value.split('=')
					id = id[1]
					self.player_data.append(id)

	def handle_data(self, data):
		if self.rec:
			self.player_data.append(data)
			self.count = self.count + 1

	def handle_endtag(self, tag):
		if tag == 'tr' and self.rec:
			self.player.append(self.player_data)
			self.rec = 0
			self.player_data = []
			self.count = 0
		if tag == 'tbody':
			self.table = 0
       
def teams_update():                
    	URL1 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLSASALL&viewName=rtssPlayerStats&sort=gamesPlayed&pg="
    	URL2 = "http://www.nhl.com/ice/playerstats.htm?season=20132014&gameType=2&position=G&viewName=summary&pg="
    	player_id_data = []
    	goalie_id_data = []
    	uris1 = []
    	uris2 = []

    	for i in range(1,20):
        	uris1.append(URL1 + str(i))

	for i in range(1,5):
		uris2.append(URL2 + str(i))

    	reqs1 = [ grequests.get(x) for x in uris1 ]
    	reqs2 = [ grequests.get(x) for x in uris2 ]
    	resps1 = grequests.map(reqs1)
    	resps2 = grequests.map(reqs2)
	
    	for x in resps1:
        	p = NHLOvernightParser()
		p.feed(x.content)

		for y in p.player:
	    		if y not in player_id_data:
				player_id_data.append(y)

    	for x in resps2:
        	p = NHLOvernightParser()
        	p.feed(x.content)

        	for y in p.player:
            		if y not in goalie_id_data:
           			goalie_id_data.append(y)

    	full_player_data = []
    	for a in player_id_data:
		if Skater.objects.filter(nhl_id = a[1]).exists():
			team = a[3]
			if team.find(","):
				parts = team.split(", ")
				team = parts[-1]
			current_team = Hockey_Team.objects.get(name=team)
			s = Skater.objects.get(nhl_id = a[1])
			if current_team != s.hockey_team:
				logger.info( "changing team for %s... was %s and is now %s" % (s.name, s.hockey_team.name, current_team.name) )
				s.hockey_team = current_team
				s.save()
			

	for a in goalie_id_data:
                if Skater.objects.filter(nhl_id = a[1]).exists():
                        team = a[3]
                        if team.find(","):
                                parts = team.split(", ")
                                team = parts[-1]
                        current_team = Hockey_Team.objects.get(name=team)
                        s = Skater.objects.get(nhl_id = a[1])
                        if current_team != s.hockey_team:
                                logger.info( "changing team for %s... was %s and is now %s" % (s.name, s.hockey_team.name, current_team.name) )
				s.hockey_team = current_team
				s.save()


logger.info("Starting team updates")		
teams_update()
