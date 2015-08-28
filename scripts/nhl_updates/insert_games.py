#!/usr/bin/python
# -*- coding: utf-8 -*-

import django
import os
import sys
import unicodedata
import urllib2
from datetime import datetime

if "/var/www/django/bhp" not in sys.path:
        sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

import vars
from parsers import *
from hockeypool.models import *
from nhl_game import nhl_game

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


for x in vars.seasons:
	for i in range(1,x['games']+1):
		print "Parsing game: %s" % x['year'] + "02" + str(i).zfill(4)
		n = nhl_game("02", str(i).zfill(4), x['year'])
		g = Game.objects.get(nhl_game_id=x['year'][0:4] + "02" + str(i).zfill(4))
			
		for s in n.homeTeamSkaters:
			p = Point.objects.filter(skater_id=n.homeTeamSkaters[s]['nhl_id']).filter(game_id=g.id)
			if len(p) == 0:
				goals = cat_goals.value*int(n.homeTeamSkaters[s]['goals']) + cat_shg.value*int(n.homeTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.homeTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.homeTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.homeTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.homeTeamSkaters[s]['emptynetgoals'])
				assists = cat_assists.value*int(n.homeTeamSkaters[s]['assists']) + cat_sha.value*int(n.homeTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.homeTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.homeTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.homeTeamSkaters[s]['powerplayassists'])
				plusminus = cat_plusminus.value*int(n.homeTeamSkaters[s]['plusminus'])
				shootout = cat_sog.value*int(n.homeTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.homeTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.homeTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.homeTeamSkaters[s]['shootoutgoalsagainst'])
				goalie = cat_w.value*int(n.homeTeamSkaters[s]['wins']) + cat_otl.value*int(n.homeTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.homeTeamSkaters[s]['saves']) + cat_so.value*int(n.homeTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.homeTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.homeTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.homeTeamSkaters[s]['goalsagainst'])
				true_grit = cat_pims.value*int(n.homeTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.homeTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.homeTeamSkaters[s]['hits']) + cat_blocks.value*int(n.homeTeamSkaters[s]['blocks']) + cat_fights.value*int(n.homeTeamSkaters[s]['fights']) + cat_gwy.value*int(n.homeTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.homeTeamSkaters[s]['takeaways']) 
				offensive_special = cat_shots.value*int(n.homeTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.homeTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.homeTeamSkaters[s]['misses']) + cat_fow.value*int(n.homeTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.homeTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.homeTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.homeTeamSkaters[s]['secondstars']) + cat_third_star.value*int(n.homeTeamSkaters[s]['thirdstars'])
				fantasy_points = goals + assists + plusminus + goalie + true_grit + offensive_special
				p = Point.objects.create(skater_id=n.homeTeamSkaters[s]['nhl_id'], game_id = g.id, fantasy_points=fantasy_points, goals=goals, assists=assists, shootout=shootout, plus_minus=plusminus, offensive_special=offensive_special, true_grit_special=true_grit, goalie=goalie, date=g.date)
				p.save()
			elif len(p) == 1:
				p = p[0]
				p.goals = cat_goals.value*int(n.homeTeamSkaters[s]['goals']) + cat_shg.value*int(n.homeTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.homeTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.homeTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.homeTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.homeTeamSkaters[s]['emptynetgoals'])
				p.assists = cat_assists.value*int(n.homeTeamSkaters[s]['assists']) + cat_sha.value*int(n.homeTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.homeTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.homeTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.homeTeamSkaters[s]['powerplayassists'])
				p.plus_minus = cat_plusminus.value*int(n.homeTeamSkaters[s]['plusminus'])
				p.shootout = cat_sog.value*int(n.homeTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.homeTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.homeTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.homeTeamSkaters[s]['shootoutgoalsagainst'])
				p.goalie = cat_w.value*int(n.homeTeamSkaters[s]['wins']) + cat_otl.value*int(n.homeTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.homeTeamSkaters[s]['saves']) + cat_so.value*int(n.homeTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.homeTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.homeTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.homeTeamSkaters[s]['goalsagainst'])
				p.true_grit = cat_pims.value*int(n.homeTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.homeTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.homeTeamSkaters[s]['hits']) + cat_blocks.value*int(n.homeTeamSkaters[s]['blocks']) + cat_fights.value*int(n.homeTeamSkaters[s]['fights']) + cat_gwy.value*int(n.homeTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.homeTeamSkaters[s]['takeaways'])
				p.offensive_special = cat_shots.value*int(n.homeTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.homeTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.homeTeamSkaters[s]['misses']) + cat_fow.value*int(n.homeTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.homeTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.homeTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.homeTeamSkaters[s]['secondstars']) + cat_third_star.value*int(n.homeTeamSkaters[s]['thirdstars'])	
				p.fantasy_points = p.goals + p.assists + p.plus_minus + p.goalie + p.true_grit + p.offensive_special
				p.save()
			else:
				print "Error: too many points with (skater_id, game_id) of (%s, %s)" % (n.homeTeamSkaters[s]['nhl_id'], g.id)

		for s in n.awayTeamSkaters:
			p = Point.objects.filter(skater_id=n.awayTeamSkaters[s]['nhl_id']).filter(game_id=g.id)
			if len(p) == 0:
				goals = cat_goals.value*int(n.awayTeamSkaters[s]['goals']) + cat_shg.value*int(n.awayTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.awayTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.awayTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.awayTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.awayTeamSkaters[s]['emptynetgoals'])
				assists = cat_assists.value*int(n.awayTeamSkaters[s]['assists']) + cat_sha.value*int(n.awayTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.awayTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.awayTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.awayTeamSkaters[s]['powerplayassists'])
				plusminus = cat_plusminus.value*int(n.awayTeamSkaters[s]['plusminus'])
				shootout = cat_sog.value*int(n.awayTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.awayTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.awayTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.awayTeamSkaters[s]['shootoutgoalsagainst'])
				goalie = cat_w.value*int(n.awayTeamSkaters[s]['wins']) + cat_otl.value*int(n.awayTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.awayTeamSkaters[s]['saves']) + cat_so.value*int(n.awayTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.awayTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.awayTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.awayTeamSkaters[s]['goalsagainst'])
				true_grit = cat_pims.value*int(n.awayTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.awayTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.awayTeamSkaters[s]['hits']) + cat_blocks.value*int(n.awayTeamSkaters[s]['blocks']) + cat_fights.value*int(n.awayTeamSkaters[s]['fights']) + cat_gwy.value*int(n.awayTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.awayTeamSkaters[s]['takeaways']) 
				offensive_special = cat_shots.value*int(n.awayTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.awayTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.awayTeamSkaters[s]['misses']) + cat_fow.value*int(n.awayTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.awayTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.awayTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.awayTeamSkaters[s]['secondstars']) + cat_third_star.value*int(n.awayTeamSkaters[s]['thirdstars'])
				fantasy_points = goals + assists + plusminus + goalie + true_grit + offensive_special
				p = Point.objects.create(skater_id=n.awayTeamSkaters[s]['nhl_id'], game_id = g.id, fantasy_points=fantasy_points, goals=goals, assists=assists, shootout=shootout, plus_minus=plusminus, offensive_special=offensive_special, true_grit_special=true_grit, goalie=goalie, date=g.date)
				p.save()
			elif len(p) == 1:
				p = p[0]
                                p.goals = cat_goals.value*int(n.awayTeamSkaters[s]['goals']) + cat_shg.value*int(n.awayTeamSkaters[s]['shorthandedgoals']) + cat_ppg.value*int(n.awayTeamSkaters[s]['powerplaygoals']) + cat_gwg.value*int(n.awayTeamSkaters[s]['gamewinninggoals']) + cat_psg.value*int(n.awayTeamSkaters[s]['penaltyshotgoals']) + cat_eng.value*int(n.awayTeamSkaters[s]['emptynetgoals'])
                                p.assists = cat_assists.value*int(n.awayTeamSkaters[s]['assists']) + cat_sha.value*int(n.awayTeamSkaters[s]['shorthandedassists']) + cat_gwa.value*int(n.awayTeamSkaters[s]['gamewinningassists']) + cat_ena.value*int(n.awayTeamSkaters[s]['emptynetassists']) + cat_ppa.value*int(n.awayTeamSkaters[s]['powerplayassists'])
                                p.plus_minus = cat_plusminus.value*int(n.awayTeamSkaters[s]['plusminus'])
                                p.shootout = cat_sog.value*int(n.awayTeamSkaters[s]['shootoutgoals']) + cat_som.value*int(n.awayTeamSkaters[s]['shootoutmisses']) + cat_sos.value*int(n.awayTeamSkaters[s]['shootoutsaves']) + cat_soga.value*int(n.awayTeamSkaters[s]['shootoutgoalsagainst'])
                                p.goalie = cat_w.value*int(n.awayTeamSkaters[s]['wins']) + cat_otl.value*int(n.awayTeamSkaters[s]['otlosses']) + cat_saves.value*int(n.awayTeamSkaters[s]['saves']) + cat_so.value*int(n.awayTeamSkaters[s]['shutouts']) + cat_pss.value*int(n.awayTeamSkaters[s]['penaltyshotsaves']) + cat_psga.value*int(n.awayTeamSkaters[s]['penaltyshotgoalsagainst']) + cat_ga.value*int(n.awayTeamSkaters[s]['goalsagainst'])
                                p.true_grit = cat_pims.value*int(n.awayTeamSkaters[s]['pims']) + cat_pimsdrawn.value*int(n.awayTeamSkaters[s]['pimsdrawn']) + cat_hits.value*int(n.awayTeamSkaters[s]['hits']) + cat_blocks.value*int(n.awayTeamSkaters[s]['blocks']) + cat_fights.value*int(n.awayTeamSkaters[s]['fights']) + cat_gwy.value*int(n.awayTeamSkaters[s]['giveaways']) + cat_twy.value*int(n.awayTeamSkaters[s]['takeaways'])
                                p.offensive_special = cat_shots.value*int(n.awayTeamSkaters[s]['shots']) + cat_shots_blocked.value*int(n.awayTeamSkaters[s]['blockedshots']) + cat_misses.value*int(n.awayTeamSkaters[s]['misses']) + cat_fow.value*int(n.awayTeamSkaters[s]['faceoffwins']) + cat_fol.value*int(n.awayTeamSkaters[s]['faceofflosses']) + cat_first_star.value*int(n.awayTeamSkaters[s]['firststars']) + cat_second_star.value*int(n.awayTeamSkaters[s]['secondstars']) + cat_third_star.value*int(n.awayTeamSkaters[s]['thirdstars'])
                                p.fantasy_points = p.goals + p.assists + p.plus_minus + p.goalie + p.true_grit + p.offensive_special
                                p.save()
                        else:
                                print "Error: too many points with (skater_id, game_id) of (%s, %s)" % (n.awayTeamSkaters[s]['nhl_id'], g.id)
