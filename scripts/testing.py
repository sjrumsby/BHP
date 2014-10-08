#!/usr/bin/python

import django
import os
import sys
import HTMLParser, urllib2, re
import logging

if "/django/BHP" not in sys.path:
	sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from django.conf import settings
from hockeypool.models import *


players = Player.objects.all()

for x in players:
	team = Team.objects.filter(player=x)
	print "%s: %s" % (x.name, len(team))


