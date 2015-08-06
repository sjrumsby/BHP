#!/usr/bin/python

import django
import os
import sys
import HTMLParser, urllib2, re
import logging
from math import floor
from random import random

if "/django/BHP" not in sys.path:
	sys.path.append("/django/BHP")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from django.conf import settings
from hockeypool.models import *
from draft.models import *

logger = logging.getLogger(__name__)

players = Player.objects.all()
Draft_Pick.objects.all().delete()
draftOrder = []

while(1):
	num = floor(random()*len(players))
	if num not in draftOrder:
		draftOrder.append(num)
	if len(draftOrder) == 8:
		break

for x in draftOrder:
	print x

for i in range(0,19):
	if i%2 == 0:
		for x in draftOrder:
			Draft_Pick.objects.create(player = players[int(x)], round_id=i+1)
	else:
		for x in reversed(draftOrder):
			Draft_Pick.objects.create(player = players[int(x)], round_id=i+1)
