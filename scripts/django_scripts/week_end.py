#!/usr/bin/python
import django
import sys
import os

if "/var/www/django/bhp" not in sys.path:
        sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

from bhp import settings

from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc
import HTMLParser, urllib2, re
from django.db.models import Sum, Q
from hockeypool.models import *
from draft.models import *
from match.models import *
from waivers.models import *
from trades.models import *

import logging
logger = logging.getLogger(__name__)

p = Pool.objects.get(pk=1)
week = p.current_week

logger.info("Ending week: %s" % week.number)
logger.info("Adding all new activations")

a = Activation.objects.all()

for x in a:
	logger.info("Adding %s to %s, with position: %s" % (x.skater.get_name(), x.player.name, x.position))
	new_at = Activated_Team.objects.create(skater = x.skater, player = x.player, week=Week.objects.filter(number=p.current_week.number+1).filter(year_id=p.current_year_id)[0], position=Position.objects.get(code=x.position))
	new_at.save()

logger.info("Activations added")
new_week = Week.objects.filter(number=week.number+1).filter(year_id=p.current_year_id)[0]
logger.info("Incrementing week from %s to %s" % (week.number, new_week.number))
p.current_week = new_week
p.save()

logger.info("Week incremented")
logger.info("Ending matches")

matches = Match.objects.filter(week_id=week.id)
for m in matches:
	logger.info("Match: %s vs %s" % (m.away_player, m.home_player))
	tmp_arr = { 'match' : m, 'home' : { 'score' : 0 }, 'away' : { 'score' : 0 } }
	tmp_arr['home']['category_points'] = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=week).values_list('date', flat=True)).filter(player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
	tmp_arr['away']['category_points'] = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=week).values_list('date', flat=True)).filter(player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
	logger.info(tmp_arr)

	if tmp_arr['home']['category_points']['fantasy_points'] > tmp_arr['away']['category_points']['fantasy_points']:
		tmp_arr['home']['score'] = tmp_arr['home']['score'] + 2
	elif tmp_arr['home']['category_points']['fantasy_points'] < tmp_arr['away']['category_points']['fantasy_points']:
		tmp_arr['away']['score'] = tmp_arr['away']['score'] + 2

	if tmp_arr['home']['category_points']['goals'] > tmp_arr['away']['category_points']['goals']:
		tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
	elif tmp_arr['home']['category_points']['goals'] < tmp_arr['away']['category_points']['goals']:
		tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

	if tmp_arr['home']['category_points']['assists'] > tmp_arr['away']['category_points']['assists']:
		tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
	elif tmp_arr['home']['category_points']['assists'] < tmp_arr['away']['category_points']['assists']:
		tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

	if tmp_arr['home']['category_points']['plus_minus'] > tmp_arr['away']['category_points']['plus_minus']:
		tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
	elif tmp_arr['home']['category_points']['plus_minus'] < tmp_arr['away']['category_points']['plus_minus']:
		tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

	if tmp_arr['home']['category_points']['offensive_special'] > tmp_arr['away']['category_points']['offensive_special']:
		tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
	elif tmp_arr['home']['category_points']['offensive_special'] < tmp_arr['away']['category_points']['offensive_special']:
		tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

	if tmp_arr['home']['category_points']['true_grit'] > tmp_arr['away']['category_points']['true_grit']:
		tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
	elif tmp_arr['home']['category_points']['true_grit'] < tmp_arr['away']['category_points']['true_grit']:
		tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

	if tmp_arr['home']['category_points']['goalie'] > tmp_arr['away']['category_points']['goalie']:
		tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
	elif tmp_arr['home']['category_points']['goalie'] < tmp_arr['away']['category_points']['goalie']:
		tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

	if tmp_arr['home']['score'] == tmp_arr['away']['score']:
		if tmp_arr['home']['category_points']['shootout'] > tmp_arr['away']['category_points']['shootout']:
			tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
		elif tmp_arr['home']['category_points']['shootout'] < tmp_arr['away']['category_points']['shootout']:
			tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

	m.home_cat = tmp_arr['home']['score']
	m.away_cat = tmp_arr['away']['score']

	if tmp_arr['home']['score'] > tmp_arr['away']['score']:
		m.winner_player = m.home_player
	elif tmp_arr['away']['score'] > tmp_arr['home']['score']:
		m.winner_player = m.away_player

	m.save()
	if tmp_arr['home']['score'] > tmp_arr['away']['score']:
		logger.info("Match won by: %s, score %s -%s" % (m.home_player, m.home_cat, m.away_cat))
	else:
		logger.info("Match won by: %s, score %s -%s" % (m.away_player, m.away_cat, m.home_cat))

logger.info("All matches processed")
logger.info("Cleaning up waiver pickups")

pickups = Waiver_Pickup.objects.filter(state=1)

for x in pickups:
	logger.info("Clearing skater %s from team %s" % (x.skater, x.player))
	x.state=2
	x.save()

logger.info("Waiver pickups processed")
logger.info("Cleaning up waiver drops")

drops = Waiver.objects.filter(state=2)

for x in drops:
	logger.info("Clearing skater %s from team %s" % (x.skater, x.player))
	x.state = 3
	x.save()
logger.info("Waiver drops processed")

logger.info("Week_end complete")
