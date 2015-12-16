#!/usr/bin/python

import django
import sys
import os
from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc

if "/var/www/django.bhp" not in sys.path:
        sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from bhp import settings

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

Team.objects.all().delete()

drafts = Draft_Pick.objects.filter(round__year_id=2)

for x in drafts:
	t = Team.objects.create(player=x.player, skater=x.pick)
	t.save()
