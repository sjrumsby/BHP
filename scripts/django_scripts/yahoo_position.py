#!/usr/bin/python

import django
import os
import sys
import HTMLParser, urllib2, re
import logging
import json

if "/var/www/django/bhp" not in sys.path:
	sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from django.conf import settings
from hockeypool.models import *
from urllib2 import urlopen

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

#Use nhl.com position code as fallback
p = Pool.objects.get(pk=1)
y = Year.objects.get(pk=p.current_year_id)

url = "http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId=" + y.description + "%20and%20gameTypeId=2"
req = urlopen(url)
data = json.loads(req.read())["data"]

for x in players:
	s = Skater.objects.filter(full_name=x[0])
	if len(s) == 1:
		s = s[0]
		Skater_Position.objects.filter(skater_id=s.nhl_id).delete()
		position = x[1].replace("RW", "R").replace("LW", "L").split(",")
		for p in position:
			sp = Skater_Position.objects.create(skater_id=s.nhl_id, position=Position.objects.get(code=p))
			sp.save()
	else:
		print "No skater found: %s, %s" % (x[0], x[1])
		if x[0] == "T.J. Brodie":
			Skater_Position.objects.filter(skater_id=8474673).delete()
			sp = Skater_Position.objects.create(skater_id=8474673, position=Position.objects.get(code='D'))
			sp.save()

for d in data:
	check = Skater_Position.objects.filter(skater_id=d["playerId"]).count()
	if check == 0:
		try:
			p = Skater.objects.get(pk=d["playerId"])
			print "Adding position %s record for: %s" % (d["playerPositionCode"], d["playerName"])
			sp = Skater_Position.objects.create(skater_id=d["playerId"], position=Position.objects.get(code=d["playerPositionCode"]))
			sp.save()
		except Skater.DoesNotExist:
			print "Creating skater for %s (ID: %s)" % (d["playerName"], d["playerId"])
			s = Skater.objects.create(nhl_id=d["playerId"],first_name=d["playerFirstName"], last_name=d["playerLastName"], full_name=d["playerName"],hockey_team=Hockey_Team.objects.filter(name=d["playerTeamsPlayedFor"].split(", ")[-1])[0])
			sp = Skater_Position.objects.create(skater=s, position=Position.objects.get(code=d["playerPositionCode"]))
                        sp.save()
	p = Skater.objects.get(pk=d["playerId"])
	if p.hockey_team.name != d["playerTeamsPlayedFor"].split(", ")[-1]:
		print "%s: %s" % (p.full_name, d["playerTeamsPlayedFor"])
		p.hockey_team = Hockey_Team.objects.filter(name=d["playerTeamsPlayedFor"].split(", ")[-1])[0]
		p.save()











