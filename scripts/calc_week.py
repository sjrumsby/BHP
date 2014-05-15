#!/usr/bin/python
import django
import json
from sys import path

django_path = '/django/django_bhp/'
if django_path not in path:
        path.append(django_path)

from django_bhp import settings
from django.core.management import setup_environ
setup_environ(settings)

from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc
import HTMLParser, grequests, urllib2, re
from django.db.models import Sum, Q
from hockeypool.models import *

for x in Player.objects.all():
	t = Activated_Team.objects.filter(player=x).values_list("skater_id", flat=True)
	if len(t) == 0:
		t = Activation.objects.filter(player=x).values_list("skater_id", flat=True)

	points = Point.objects.filter(week__id=24).filter(skater_id__in=t).aggregate(fantasy_points=Sum('fantasy_points'), goals=Sum('goals'), assists=Sum('assists'), shootout=Sum('shootout'), plus_minus=Sum('plus_minus'), offensive_special=Sum('offensive_special'), true_grit=Sum('true_grit_special'), goalie=Sum('goalie'))

	if points['fantasy_points'] != None:
		print x
		print json.dumps(points, sort_keys=True, indent=4)
