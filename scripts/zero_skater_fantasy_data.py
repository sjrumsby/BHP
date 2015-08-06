#!/usr/bin/python

import django
import sys
import os
from django.utils.timezone import utc
import urllib2
import json

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from BHP import settings

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

Team_Point.objects.all().delete()
Point.objects.all().delete()

s = Skater.objects.all()

for x in s:
        print "Zeroing skater: %s" % x
s = Skater.objects.all()

for x in s:
        print "Zeroing skater: %s" % x
        x.games = 0
        x.goals = 0
        x.assists = 0
        x.points = 0
        x.plus_minus = 0
        x.shg = 0
        x.sha = 0
        x.ppg = 0
        x.ppa = 0
        x.gwg = 0
        x.psg = 0
        x.pims = 0
        x.hits = 0
        x.shots = 0
        x.blocks = 0
        x.fights = 0
        x.giveaways = 0
        x.takeaways = 0
        x.faceoff_win = 0
        x.faceoff_loss = 0
        x.shootout_made = 0
        x.shootout_fail = 0
        x.wins = 0
        x.otloss = 0
        x.shutouts = 0
        x.penshot_save = 0
        x.penshot_ga = 0
        x.shootout_save = 0
        x.shootout_ga = 0
        x.saves = 0
        x.goals_against = 0
        x.fantasy_points = 0
	x.time_on_ice = '0:00'
        x.save()

