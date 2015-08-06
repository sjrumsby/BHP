#!/usr/bin/python

import django
import sys
import os
from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc
from time import time
import HTMLParser, grequests, urllib2, re

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from BHP import settings

from hockeypool.models import *
from match.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

#Define all fantasy point values

cat_vals = {
		'goals' 		: 10,
		'assists' 		: 10,
		'plus_minus' 		: 7,
		'ppg' 			: 7,
		'shg' 			: 12,
		'ppa' 			: 7,
		'sha' 			: 12,
		'psg' 			: 10,
		'gwg' 			: 10,
		'hits' 			: 1,
		'blocks' 		: 1,
		'giveaways' 		: -1,
		'takeaways' 		: 1,
		'faceoff_win' 		: 1,
		'faceoff_loss' 		: -1,
		'shots' 		: 1,
		'pims' 			: -1,
		'fights' 		: 20,
		'shootout_made' 	: 1,
		'shootout_fail' 	: -1,
		'wins' 			: 15,
		'shutouts' 		: 25,
		'otloss'		: 8,
		'penshot_save' 		: 6,
		'penshot_ga' 		: -3,
		'shootout_save' 	: 1,
		'shootout_ga' 		: -1,
		'saves' 		: 1,
		'goals_against' 	: -7,
	}

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
                        
def player_teams_update():
	st = time()
	pool = Pool.objects.get(pk=1)
	week = pool.current_week
    	URL1 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASALL&viewName=goals&sort=goals&pg="
    	URL6 = "http://www.nhl.com/ice/playerstats.htm?season=20142015&gameType=2&position=G&viewName=summary&pg="

    	player_goal_data = []
    	player_id_data = []
    	goalie_win_data = []
    	goalie_id_data = []

    	uris1 = []
    	uris6 = []

    	for i in range(1,20):
        	uris1.append(URL1 + str(i))

	for i in range(1,3):
		uris6.append(URL6 + str(i))

    	reqs1 = [ grequests.get(x) for x in uris1 ]
    	reqs6 = [ grequests.get(x) for x in uris6 ]

    	resps1 = grequests.map(reqs1)
    	resps6 = grequests.map(reqs6)

    	for x in resps1:
        	p = NHLOvernightParser()
		p.feed(x.content)

		for y in p.player:
			s = Skater.objects.get(nhl_id=y[1])
			if y[3] != s.hockey_team.name:
				logger.info("Updating team for skater: %s. Was %s is now %s" % (s.name, s.hockey_team.name, y[3]))
				h = Hockey_Team.objects.filter(name=y[3])[0]
				s.hockey_team = h
				s.save()
			

    	for x in resps6:
        	p = NHLOvernightParser()
        	p.feed(x.content)

        	for y in p.player:
                        s = Skater.objects.get(nhl_id=y[1])
                        if y[3] != s.hockey_team.name:
                                logger.info("Updating team for skater: %s. Was %s is now %s" % (s.name, s.hockey_team.name, y[3]))
                                h = Hockey_Team.objects.filter(name=y[3])[0]
                                s.hockey_team = h
                                s.save()

	diff_time = time() - st
	logger.info("Total time elapsed: %s" % diff_time)

logger.info("Starting player updates")
player_teams_update()
logger.info("Player updates finished")
