#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import django
import json
import os
import sys
import urllib2

if "/usr/local/apps/bhp" not in sys.path:
    sys.path.append("/usr/local/apps/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from hockeypool.models import *

import logging
logger = logging.getLogger(__name__)

logger.info("Starting full season update")

pool = Pool.objects.get(pk=1)
year = pool.current_year

start_date = year.description[:4] + "-10-01"
end_date = year.description[4:] + "-04-30"
url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=%s&endDate=%s&expand=schedule.linescore&gameType=R" % (start_date, end_date)

print url

req = urllib2.urlopen(url)
reqJSON = req.read()
reqData = json.loads(reqJSON)

for date in reqData["dates"]:
    print date["date"]
    for game in date["games"]:
        print "  " + str(game["gamePk"])

        g = Game.objects.get(nhl_game_id=game["gamePk"])
        g.home_score = game["linescore"]["teams"]["home"]["goals"]
        g.away_score = game["linescore"]["teams"]["away"]["goals"]
        g.save()


