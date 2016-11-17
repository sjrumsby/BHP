#!/usr/bin/python

import django
import sys
import os

if "/var/www/django/bhp" not in sys.path:
        sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from hockeypool.models import *
from draft.models import *
from waivers.models import *

import logging
logger = logging.getLogger(__name__)

logger.info("Process waivers")
waivers = Waiver.objects.all()

if len(waivers) > 0:
	accepted = Waiver.objects.filter(state=0)

        if len(accepted) > 0:
                logger.info("Removing all accepted waivers")
                for x in accepted:
                        x.state = 2
                        x.save()
                        t = Team.objects.filter(skater = x.skater)
                        if len(t) == 1:
                                logger.info("deleting skater: %s" % t[0].skater.full_name)
                                t.delete()
			else:
				logger.info("Error: %s team players found" % len(t))
        else:
                logger.info("No accepted waivers to process")
else:
	logger.info("There are no waivers to process today")

