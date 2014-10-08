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
from match.models import *
from rankings.models import *

Team_Point.objects.all().delete()
weeks = Week.objects.all()

for x in weeks:
	Point.objects.filter(week=x).delete()
Power_Rank.objects.all().delete()

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
	x.save()

m = Match.objects.all()

for x in m:
	x.winner_player = None
	x.home_cat = 0
	x.away_cat = 0
	x.save()
	
