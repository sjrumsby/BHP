#!/usr/bin/python

import django
from sys import path
from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc
import HTMLParser, grequests, urllib2, re

django_path = '/django/django_bhp/'
if django_path not in path:
        path.append(django_path)

from django_bhp import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.db.models import Q

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

pool = Pool.objects.get(pk=1)
current_week = pool.current_week
skaters = []
h = Hockey_Team.objects.all()

for x in h:
	s = Skater.objects.filter(hockey_team=x)[0]
	skaters.append(s)

for x in skaters:
	print "%s: %s" % (x.hockey_team, Game.objects.filter(date__in=Week_Dates.objects.filter(week__number=current_week.number + 1).values_list('date', flat="True")).filter(Q(home_team=x.hockey_team)|Q(away_team=x.hockey_team)).count())
