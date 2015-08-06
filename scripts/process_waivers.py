#!/usr/bin/python

import django
import sys
import os

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from hockeypool.models import *
from draft.models import *
from waivers.models import *

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
			logger.info("Accepting skater: %s" % x.skater.name)
			x.state = 1
			x.save()
	else:
		logger.info("No pending waivers to accept")
else:
	logger.info("There are no waivers to process today")

logger.info("Processing pickups")
pickups = Waiver_Pickups.objects.filter(state=0)

if len(pickups) > 0:
	if len(pickups) == 1:
		p = pickups[0]
		new_t = Team.objects.create(skater=p.skater, player=p.player)
		new_t.save()
		p.state = 1
		p.save()
	else:
		for x in pickups:
			if Waiver_Pickups.objects.filter(skater=x.skater).count() == 1:
				logger.info("Adding skater: %s to team: %s" % (p.skater, p.player))
				p = pickups[0]
				new_t = Team.objects.create(skater=p.skater, player=p.player)
				new_t.save()
				p.state = 1
				p.save()
			else:
				logger.info("There is a conflift. Exiting for Commissioner intervention")
else:
	logger.info("No pickups to process")



