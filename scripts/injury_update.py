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

class injuryParser(HTMLParser.HTMLParser):
        def __init__(self):
                HTMLParser.HTMLParser.__init__(self)
                self.rightDiv = 0
                self.recording = 0
                self.injuries = []
                self.injuryData = []
                self.data = ''

        def handle_starttag(self, tag, attributes):
                if tag == 'div':
                        for name, value in attributes:
                                if name == 'id' and value == 'tsnStats':
                                        self.rightDiv = 1

                if self.rightDiv and tag=='tr':
                        for name, value in attributes:
                                if name == 'class' and (value == 'bg1' or value == 'bg2'):
                                        self.recording = 1

        def handle_endtag(self, tag):
                if tag == 'tr' and self.recording:
                        self.recording = 0
                        self.injuries.append(self.injuryData)
                        self.injuryData = []

        def handle_data(self, data):
                if self.recording:
                        self.injuryData.append(data)

def injury_update():
        logger.info("processing injuries")
        url = "http://www.tsn.ca/nhl/injuries/"
        resp = urllib2.urlopen(url)
        html = resp.read()
        p = injuryParser()
        p.feed(re.sub("&nbsp;", " ", html))

        Injury.objects.all().delete()

        for x in p.injuries:
                players = Skater.objects.filter(name=x[0])
                if len(players) == 1:
                        player = players[0]
                        i = Injury.objects.create(skater_id = player.id, name = x[0], date = x[1], status = x[2], description = x[3])
                        i.save()
                else:
                        logger.info("Unable to parse injury information for player: %s" % players)

injury_update()

