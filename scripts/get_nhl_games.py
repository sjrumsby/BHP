#!/usr/bin/python

import django
import os
import sys
import HTMLParser, urllib2, re, time
import logging

if "/django/BHP" not in sys.path:
	sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from django.conf import settings
from hockeypool.models import *

class seasonParser(HTMLParser.HTMLParser):
        def __init__(self):
                HTMLParser.HTMLParser.__init__(self)
                self.recording = 0
                self.games = []
		self.data = []

        def handle_starttag(self, tag, attributes):
                if tag == 'table':
                        for name, value in attributes:
                                if name == 'class' and value == 'data schedTbl':
                                        self.recording = 1

        def handle_endtag(self, tag):
                if tag == 'tr' and self.recording:
			if "VISITING TEAM" not in self.data:
				self.games.append(self.data)
                        self.data = []

        def handle_data(self, data):
                if self.recording:
                        self.data.append(data)

resp = urllib2.urlopen("http://www.nhl.com/ice/schedulebyseason.htm")
html = resp.read()
p = seasonParser()
p.feed(html)

count = 1
for x in p.games:
	if len(x) > 2:
		print x
		homeTeam = Hockey_Team.objects.filter(full_name=x[3])
		awayTeam = Hockey_Team.objects.filter(full_name=x[2])

		if len(homeTeam) != 1 or len(awayTeam) != 1:
			print x
		else:
			homeTeam = homeTeam[0]
			awayTeam = awayTeam[0]
			date = time.strptime(x[0], "%a %b %d, %Y")
			date = str(date.tm_year) + "-" + str(date.tm_mon).zfill(2) + "-" + str(date.tm_mday).zfill(2)
			print homeTeam, awayTeam, date
			g = Game.objects.create(date=date,home_team=homeTeam, away_team=awayTeam, time=x[5], nhl_game_id="201402"+str(count).zfill(4))
			g.save()
			count += 1

