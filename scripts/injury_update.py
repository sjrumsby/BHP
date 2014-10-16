#!/usr/bin/python

import django
import sys
import os
from django.utils.timezone import utc
import urllib2
import json

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from BHP import settings

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

def injury_update():
        logger.info("processing injuries")
        url = "http://stats.tsn.ca/GET/urn:tsn:nhl:injuries?type=json"
        resp = urllib2.urlopen(url)
        data = json.loads(resp.read())

        Injury.objects.all().delete()

        for x in data['InjuryReports']:
		for y in x['Injuries']:
			name = y['Player']['FirstName'] + ' ' + y['Player']['LastName']
			date = y['ReportedDate'].split('/')
			date = date[2]+'-'+date[0]+'-'+date[1]
			players = Skater.objects.filter(name=name)
			if len(players) == 1:
				player = players[0]
				i = Injury.objects.create(skater_id = player.id, name = name, date = date, status = y['InjuryDetail']['Status'], description = y['InjuryDetail']['Description'])
				i.save()
			else:
				logger.info("Unable to parse injury information for player: %s" % players)

injury_update()

