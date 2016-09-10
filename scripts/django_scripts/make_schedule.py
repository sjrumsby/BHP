#!/usr/bin/python

import django
import os
import sys
import HTMLParser, urllib2, re, time
import logging

if "/var/www/django.bhp" not in sys.path:
	sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from django.conf import settings
from hockeypool.models import *

f = open('201617.csv', 'r')

lines = f.readlines()

teams = {
		"Anaheim Ducks": "Anaheim",
		"Arizona Coyotes":"Arizona",
		"Boston Bruins":"Boston",
		"Buffalo Sabres":"Buffalo",
		"Calgary Flames":"Calgary",
		"Carolina Hurricanes":"Carolina",
		"Chicago Blackhawks":"Chicago",
		"Colorado Avalanche":"Colorado",
		"Columbus Blue Jackets":"Columbus",
		"Dallas Stars":"Dallas",
		"Detroit Red Wings":"Detroit",
		"Edmonton Oilers":"Edmonton",
		"Florida Panthers":"Florida",
		"Los Angeles Kings":"Los Angeles",
		"Minnesota Wild": "Minnesota",
		"Montreal Canadiens":"Montreal",
		"Nashville Predators":"Nashville",
		"New Jersey Devils":"New Jersey",
		"NY Rangers":"NY Rangers",
		"NY Islanders":"NY Islanders",
		"Ottawa Senators":"Ottawa" ,
		"Philadelphia Flyers":"Philadelphia",
		"Pittsburgh Penguins":"Pittsburgh",
		"San Jose Sharks":"San Jose",
		"St. Louis Blues":"St. Louis",
		"Toronto Maple Leafs":"Toronto",
		"Tampa Bay Lightning":"Tampa Bay",
		"Vancouver Canucks":"Vancouver",
		"Washington Capitals":"Washington",
		"Winnipeg Jets": "Winnipeg"
	}

months = {
		"Oct": "10",
		"Nov": "11",
		"Dec": "12",
		"Jan": "01",
		"Feb": "02",
		"Mar": "03",
		"Apr": "04",
	}

c = 2016020001

for x in lines:
	y = x.replace("\r", "").replace("\n","")
	y = y.replace("New York", "NY")
	y = y.replace("St.Louis", "St. Louis")
	y = y.split(",")
	print y
	a1 = teams[y[1]]
	a2 = teams[y[2]]
	
	h = Hockey_Team.objects.get(full_name=a1)
	a = Hockey_Team.objects.get(full_name=a2)

	d = y[0].split("-")
	d = d[-1] + "-" + months[d[1]] + "-" + d[0]

	g = Game.objects.create(date=d, home_team=h, away_team=a, time="00:00:00", nhl_game_id=c, year_id=6)
	c += 1
