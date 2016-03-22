#!/usr/bin/python
# -*- coding: utf-8 -*-

import django
import os
import sys
import unicodedata
import urllib2
import datetime

if "/var/www/django/bhp" not in sys.path:
        sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

import vars
from parsers import *
from hockeypool.models import *
from match.models import *
from nhl_game import nhl_game

import logging
logger = logging.getLogger(__name__)

def check_skater(nhl_id):
	if Skater.objects.filter(nhl_id=nhl_id).count() == 0:
		return False
	else:
		return True

def save_point(p):
        wd = Week_Date.objects.filter(date=p.date)
        if len(wd) == 1:
                w = Week.objects.get(id=wd[0].week_id)
                a = Activated_Team.objects.filter(week=w).filter(skater=p.skater).exclude(position__code='B')
                for x in a:
			check = Team_Point.objects.filter(point=p,player=x.player,pool=x.player.pool).count()
			if check == 0:
				t = Team_Point.objects.create(point=p,player=x.player,pool=x.player.pool)
				t.save()

cat_goals = Category_Point.objects.get(id=1)
cat_assists = Category_Point.objects.get(id=2)
cat_plusminus = Category_Point.objects.get(id=3)
cat_shg = Category_Point.objects.get(id=4)
cat_sha = Category_Point.objects.get(id=5)
cat_gwa = Category_Point.objects.get(id=6)
cat_ena = Category_Point.objects.get(id=7)
cat_ppg = Category_Point.objects.get(id=8)
cat_ppa = Category_Point.objects.get(id=9)
cat_gwg = Category_Point.objects.get(id=10)
cat_psg = Category_Point.objects.get(id=11)
cat_eng = Category_Point.objects.get(id=12)
cat_pims = Category_Point.objects.get(id=13)
cat_pimsdrawn = Category_Point.objects.get(id=14)
cat_hits = Category_Point.objects.get(id=15)
cat_shots = Category_Point.objects.get(id=16)
cat_shots_blocked = Category_Point.objects.get(id=17)
cat_misses = Category_Point.objects.get(id=18)
cat_blocks = Category_Point.objects.get(id=19)
cat_fights = Category_Point.objects.get(id=20)
cat_gwy = Category_Point.objects.get(id=21)
cat_twy = Category_Point.objects.get(id=22)
cat_fow = Category_Point.objects.get(id=23)
cat_fol = Category_Point.objects.get(id=24)
cat_toi = Category_Point.objects.get(id=25)
cat_sog = Category_Point.objects.get(id=26)
cat_som = Category_Point.objects.get(id=27)
cat_w = Category_Point.objects.get(id=28)
cat_otl = Category_Point.objects.get(id=29)
cat_saves = Category_Point.objects.get(id=30)
cat_so = Category_Point.objects.get(id=31)
cat_pss = Category_Point.objects.get(id=32)
cat_psga = Category_Point.objects.get(id=33)
cat_sos = Category_Point.objects.get(id=34)
cat_soga = Category_Point.objects.get(id=35)
cat_ga = Category_Point.objects.get(id=36)
cat_first_star = Category_Point.objects.get(id=37)
cat_second_star = Category_Point.objects.get(id=38)
cat_third_star = Category_Point.objects.get(id=39)

def parse_game(game):
	print "%s, %s, %s" % ("02", str(game.nhl_game_id)[6:10], game.year.description)

	n = nhl_game("02", str(game.nhl_game_id)[6:10], game.year.description, True)

	for s in n.homeTeamSkaters:
		if check_skater(n.homeTeamSkaters[s]['nhl_id']):
			p = Point.objects.filter(skater_id=n.homeTeamSkaters[s]['nhl_id']).filter(game_id=game.id)
			if len(p) == 0:
				goals = cat_goals.value*int(n.homeTeamSkaters[s]['goals']) + cat_shg.value*int(n.homeTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.homeTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.homeTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.homeTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.homeTeamSkaters[s]['emptynetgoals'])
				assists = cat_assists.value*int(n.homeTeamSkaters[s]['assists']) + cat_sha.value*int(n.homeTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.homeTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.homeTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.homeTeamSkaters[s]['powerplayassists'])
				plusminus = cat_plusminus.value*int(n.homeTeamSkaters[s]['plusminus'])
				shootout = cat_sog.value*int(n.homeTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.homeTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.homeTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.homeTeamSkaters[s]['shootoutgoalsagainst'])
				goalie = cat_w.value*int(n.homeTeamSkaters[s]['wins']) + cat_otl.value*int(n.homeTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.homeTeamSkaters[s]['saves']) + cat_so.value*int(n.homeTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.homeTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.homeTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.homeTeamSkaters[s]['goalsagainst'])
				true_grit = cat_pims.value*int(n.homeTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.homeTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.homeTeamSkaters[s]['hits']) + cat_blocks.value*int(n.homeTeamSkaters[s]['blocks']) + cat_fights.value*int(n.homeTeamSkaters[s]['fights']) + cat_gwy.value*int(n.homeTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.homeTeamSkaters[s]['takeaways'])
				offensive_special = cat_shots.value*int(n.homeTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.homeTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.homeTeamSkaters[s]['misses']) + cat_fow.value*int(n.homeTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.homeTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.homeTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.homeTeamSkaters[s]['secondstars']) + cat_third_star.value*int(n.homeTeamSkaters[s]['thirdstars'])
				fantasy_points = goals + assists + plusminus + goalie + true_grit + offensive_special
				p = Point.objects.create(skater_id=n.homeTeamSkaters[s]['nhl_id'], game_id = game.id, fantasy_points=fantasy_points, goals=goals, assists=assists, shootout=shootout, plus_minus=plusminus, offensive_special=offensive_special, true_grit_special=true_grit, goalie=goalie, date=game.date)
				p.save()
				save_point(p)
			elif len(p) == 1:
				p = p[0]
				p.goals = cat_goals.value*int(n.homeTeamSkaters[s]['goals']) + cat_shg.value*int(n.homeTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.homeTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.homeTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.homeTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.homeTeamSkaters[s]['emptynetgoals'])
				p.assists = cat_assists.value*int(n.homeTeamSkaters[s]['assists']) + cat_sha.value*int(n.homeTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.homeTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.homeTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.homeTeamSkaters[s]['powerplayassists'])
				p.plus_minus = cat_plusminus.value*int(n.homeTeamSkaters[s]['plusminus'])
				p.shootout = cat_sog.value*int(n.homeTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.homeTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.homeTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.homeTeamSkaters[s]['shootoutgoalsagainst'])
				p.goalie = cat_w.value*int(n.homeTeamSkaters[s]['wins']) + cat_otl.value*int(n.homeTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.homeTeamSkaters[s]['saves']) + cat_so.value*int(n.homeTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.homeTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.homeTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.homeTeamSkaters[s]['goalsagainst'])
				p.true_grit_special = cat_pims.value*int(n.homeTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.homeTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.homeTeamSkaters[s]['hits']) + cat_blocks.value*int(n.homeTeamSkaters[s]['blocks']) + cat_fights.value*int(n.homeTeamSkaters[s]['fights']) + cat_gwy.value*int(n.homeTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.homeTeamSkaters[s]['takeaways'])
				p.offensive_special = cat_shots.value*int(n.homeTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.homeTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.homeTeamSkaters[s]['misses']) + cat_fow.value*int(n.homeTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.homeTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.homeTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.homeTeamSkaters[s]['secondstars']) +cat_third_star.value*int(n.homeTeamSkaters[s]['thirdstars'])
				p.fantasy_points = p.goals + p.assists + p.plus_minus + p.goalie + p.true_grit_special + p.offensive_special
				p.save()
				save_point(p)
			else:
				print "Error: too many points with (skater_id, game_id) of (%s, %s)" % (n.homeTeamSkaters[s]['nhl_id'], g.id)
	for s in n.awayTeamSkaters:
		if check_skater(n.awayTeamSkaters[s]['nhl_id']):
			p = Point.objects.filter(skater_id=n.awayTeamSkaters[s]['nhl_id']).filter(game_id=game.id)

			if len(p) == 0:
				goals = cat_goals.value*int(n.awayTeamSkaters[s]['goals']) + cat_shg.value*int(n.awayTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.awayTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.awayTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.awayTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.awayTeamSkaters[s]['emptynetgoals'])
				assists = cat_assists.value*int(n.awayTeamSkaters[s]['assists']) + cat_sha.value*int(n.awayTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.awayTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.awayTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.awayTeamSkaters[s]['powerplayassists'])
				plusminus = cat_plusminus.value*int(n.awayTeamSkaters[s]['plusminus'])
				shootout = cat_sog.value*int(n.awayTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.awayTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.awayTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.awayTeamSkaters[s]['shootoutgoalsagainst'])
				goalie = cat_w.value*int(n.awayTeamSkaters[s]['wins']) + cat_otl.value*int(n.awayTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.awayTeamSkaters[s]['saves']) + cat_so.value*int(n.awayTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.awayTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.awayTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.awayTeamSkaters[s]['goalsagainst'])
				true_grit = cat_pims.value*int(n.awayTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.awayTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.awayTeamSkaters[s]['hits']) + cat_blocks.value*int(n.awayTeamSkaters[s]['blocks']) + cat_fights.value*int(n.awayTeamSkaters[s]['fights']) + cat_gwy.value*int(n.awayTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.awayTeamSkaters[s]['takeaways'])
				offensive_special = cat_shots.value*int(n.awayTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.awayTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.awayTeamSkaters[s]['misses']) + cat_fow.value*int(n.awayTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.awayTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.awayTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.awayTeamSkaters[s]['secondstars']) + cat_third_star.value*int(n.awayTeamSkaters[s]['thirdstars'])
				fantasy_points = goals + assists + plusminus + goalie + true_grit + offensive_special
				p = Point.objects.create(skater_id=n.awayTeamSkaters[s]['nhl_id'], game_id = game.id, fantasy_points=fantasy_points, goals=goals, assists=assists, shootout=shootout, plus_minus=plusminus, offensive_special=offensive_special, true_grit_special=true_grit, goalie=goalie, date=game.date)
				p.save()
				save_point(p)
			elif len(p) == 1:
				p = p[0]
				p.goals = cat_goals.value*int(n.awayTeamSkaters[s]['goals']) + cat_shg.value*int(n.awayTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.awayTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.awayTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.awayTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.awayTeamSkaters[s]['emptynetgoals'])
				p.assists = cat_assists.value*int(n.awayTeamSkaters[s]['assists']) + cat_sha.value*int(n.awayTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.awayTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.awayTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.awayTeamSkaters[s]['powerplayassists'])
				p.plus_minus = cat_plusminus.value*int(n.awayTeamSkaters[s]['plusminus'])
				p.shootout = cat_sog.value*int(n.awayTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.awayTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.awayTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.awayTeamSkaters[s]['shootoutgoalsagainst'])
				p.goalie = cat_w.value*int(n.awayTeamSkaters[s]['wins']) + cat_otl.value*int(n.awayTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.awayTeamSkaters[s]['saves']) + cat_so.value*int(n.awayTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.awayTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.awayTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.awayTeamSkaters[s]['goalsagainst'])
				p.true_grit_special = cat_pims.value*int(n.awayTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.awayTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.awayTeamSkaters[s]['hits']) + cat_blocks.value*int(n.awayTeamSkaters[s]['blocks']) + cat_fights.value*int(n.awayTeamSkaters[s]['fights']) + cat_gwy.value*int(n.awayTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.awayTeamSkaters[s]['takeaways'])
				p.offensive_special = cat_shots.value*int(n.awayTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.awayTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.awayTeamSkaters[s]['misses']) + cat_fow.value*int(n.awayTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.awayTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.awayTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.awayTeamSkaters[s]['secondstars']) +cat_third_star.value*int(n.awayTeamSkaters[s]['thirdstars'])
				p.fantasy_points = p.goals + p.assists + p.plus_minus + p.goalie + p.true_grit_special + p.offensive_special
				p.save()
				save_point(p)
			else:
				print "Error: too many points with (skater_id, game_id) of (%s, %s)" % (n.awayTeamSkaters[s]['nhl_id'], g.id)


def daily_update(day=None):
    if day is None:
            games = Game.objects.filter(date=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d"))
    else:
            games = Game.objects.filter(date=day)
    for g in games:
        logger.info("Parsing game: %s" % g.nhl_game_id)
        parse_game(g)

def weekly_update(week_id=None):
    if week_id is None:
        current_week = Week_Date.objects.filter(date=datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1),"%Y-%m-%d"))
        if len(current_week) == 1:
            current_week = current_week[0]
            week_dates = Week_Date.objects.filter(week_id=current_week.week_id).filter(date__lte=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d"))
            games = Game.objects.filter(date__in=week_dates.values_list('date', flat="True"))
            for g in games:
                logger.info("Parsing game: %s" % g.nhl_game_id)
                try:
                    parse_game(g)
                except:
                    logger.error("Error parsing game: %s" % g.nhl_game_id)
    else:
        try:
            week_dates = Week_Date.objects.filter(week=Week.objects.get(id=week_id))
            games = Game.objects.filter(date__in=week_dates.values_list('date', flat="True"))
            print games
            for g in games:
                logger.info("Parsing game: %s" % g.nhl_game_id)
                try:
                    parse_game(g)
                except:
                    logger.error("Error parsing game: %s" % g.nhl_game_id)
        except Week.DoesNotExist:
            logger.error("Does not exist")

def season_update():
	week_dates = Week_Date.objects.filter(date__lte=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")).filter(week__year_id=2)
	games = Game.objects.filter(date__in=week_dates.values_list('date', flat="True")).order_by('nhl_game_id')
	for g in games:
		logger.info("Parsing game: %s" % g.nhl_game_id)
		parse_game(g)

def game_update(game_id):
	try:
		game_id = int(game_id)
		g = Game.objects.filter(nhl_game_id=game_id)
		if g.count() != 1:
			exit("Error finding game id: %s. %s games were found" % game_id, g.count())
		g = g[0]
		logger.info("Parsing game: %s" % g.nhl_game_id)
		print "Parsing game: %s" % g.nhl_game_id
		parse_game(g)

	except ValueError:
		print "Invalid game id. Must be an integer between 1 and 1230 inclusive"

if len(sys.argv) != 2 and not ((sys.argv[1] in ["-g", "--game", "-d", "--daily", "-w", "--weekly"]) and len(sys.argv) == 3):
	print "Invalid command"
	exit()

if sys.argv[1] == "-g" or sys.argv[1] == "--game":
        #Do some shit to get the current date here
        game_update(sys.argv[2])

elif sys.argv[1] == "-d" or sys.argv[1] == "--daily":
    if len(sys.argv) == 3:
        #Do some shit to get the current date here
        daily_update(sys.argv[2])
    else:
        daily_update()

elif sys.argv[1] == "-w" or sys.argv[1] == "--weekly":
	#Do some shit to get the current date here
    if len(sys.argv) == 3:
        weekly_update(sys.argv[2])
    else:
        weekly_update()

elif sys.argv[1] == "-f" or sys.argv[1] == "--full":
	#Do some shit to get the current date here
	full_update()

elif sys.argv[1] == "-s" or sys.argv[1] == "--season":
	#Do some shit to get the current date here
	season_update()
else:
	print "Unknown flag"
