#!/usr/bin/python

import django
import sys
import os
from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc
import HTMLParser, grequests, urllib2, re

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from BHP import settings

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

drafts = Draft_Pick.objects.all()
week= Week.objects.get(id=1)

for x in drafts:
	Team.objects.create(player=x.player, skater=x.pick, week=1, active=1)
