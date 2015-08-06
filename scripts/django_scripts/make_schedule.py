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

f = open('schedule.csv', 'r')

lines = f.readlines()

for x in lines:
	print x
	l = x.split(",")
	w = Week_Dates.objects.create(date=l[0],week_id=l[1])
	w.save()
