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

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

waivers = Waiver.objects.all()
if len(waivers) > 0:
	logger.info("Process waivers")
	pending = Waiver.objects.filter(state = 0)
	accepted = Waiver.objects.filter(state = 1)

        if len(accepted) > 0:
                logger.info("Removing all accepted waivers")
                for x in accepted:
                        x.state = 2
                        x.save()
                        t = Team.objects.filter(skater = x.skater)
                        if len(t) == 1:
                                logger.info("deleting skater: %s" % t[0].skater.name)
                                t.delete()
				x.state = 2
				x.save()
        else:
                logger.info("No accepted waivers to process")

	if len(pending) > 0:
		logger.info("Accepting all pending waivers")
		for x in pending:
			x.state = 1
			x.save()
	else:
		logger.info("No pending waivers to accept")
else:
	logger.info("There are no waivers to process today")
