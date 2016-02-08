#!/usr/bin/python
import django
import json
import sys
import os

if "/var/www/django/bhp" not in sys.path:
        sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from bhp import settings
from hockeypool.models import *
from urllib2 import urlopen

import logging
logger = logging.getLogger(__name__)

p = Pool.objects.get(pk=1)
url = "http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2"

req = urlopen(url)
data = json.loads(req.read())["data"]

for d in data:
	try:
		s = Skater.objects.get(pk=d["playerId"])
	except Skater.DoesNotExist:
		print "Entering skater: %s" % d["playerName"]
		Skater.objects.create(	nhl_id=d["playerId"],
					first_name=d["playerFirstName"],
					last_name=d["playerLastName"],
					full_name=d["playerName"],
					hockey_team=Hockey_Team.objects.get(name=d["playerTeamsPlayedFor"].split(",")[-1]),
					goals = 0,
					assists = 0,
					points = 0,
					plus_minus = 0,
					shg = 0,
					sha = 0,
					ppg = 0,
					ppa = 0,
					gwg = 0,
					gwa = 0,
					psg = 0,
					eng = 0,
					ena = 0,
					pims = 0,
					pims_drawn = 0,
					hits = 0,
					shots = 0,
					blocked_shots = 0,
					blocks = 0,
					fights = 0,
					giveaways = 0,
					takeaways = 0,
					faceoff_win = 0,
					faceoff_loss = 0,
					shootout_made = 0,
					shootout_fail = 0,
					wins = 0,
					otloss = 0,
					shutouts = 0,
					penshot_save = 0,
					penshot_ga = 0,
					shootout_save = 0,
					shootout_ga = 0,
					saves = 0,
					goals_against = 0,
					time_on_ice = 0,
					first_stars = 0,
					second_stars = 0,
					third_stars = 0,
					fantasy_points = 0);
	

