#!/usr/bin/python

import django
import os
import sys
import HTMLParser, urllib2, re, time
import logging

if "/var/www/django/bhp" not in sys.path:
	sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from django.conf import settings
from hockeypool.models import *

w50 = Game.objects.filter(date__in=Week_Date.objects.filter(week_id=50).values_list("date", flat=True)).count()
w51 = Game.objects.filter(date__in=Week_Date.objects.filter(week_id=51).values_list("date", flat=True)).count()
w52 = Game.objects.filter(date__in=Week_Date.objects.filter(week_id=52).values_list("date", flat=True)).count()

print w50
print w51
print w52
