#!/usr/bin/python

import django
import os
import sys
import HTMLParser, urllib2, re
import logging

if "/django/BHP" not in sys.path:
	sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from django.conf import settings
from hockeypool.models import *

logger = logging.getLogger(__name__)

class playerParser(HTMLParser.HTMLParser):
        def __init__(self):
                HTMLParser.HTMLParser.__init__(self)
                self.rightDiv = 0
                self.recording = 0
                self.playerData = []
                self.players = []

        def handle_starttag(self, tag, attributes):
                if tag == 'table':
                        for name, value in attributes:
                                if name == 'id' and value == 'draftanalysistable':
                                        self.recording = 1

        def handle_endtag(self, tag):
                if tag == 'tr' and self.recording:
			if "Avg Pick" not in self.playerData and len(self.playerData) > 2:
				self.players.append(self.playerData)
                        self.playerData = []

        def handle_data(self, data):
                if self.recording:
                        self.playerData.append(data)

players = []

for i in range(0,6):
        url = "http://hockey.fantasysports.yahoo.com/hockey/draftanalysis?tab=SD&pos=ALL&sort=DA_AP&count=%s" % str(i*50)
        resp = urllib2.urlopen(url)
        html = resp.read()
        p = playerParser()
        p.feed(html)

        for x in p.players:
		players.append([x[5], x[7].split(" - ")[-1]])

for x in players:
	s = Skater.objects.filter(name=x[0])
	if len(s) == 1:
		s = s[0]
		position = x[1].replace(",",", ").replace("RW", "R").replace("LW", "L")
		s.position = position
		s.save()
	else:
		print "No skater found: %s, %s" % (x[0], x[1])


