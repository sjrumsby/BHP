#!/usr/bin/python

import django
import sys
import os
from random import random
from datetime import datetime, timedelta
from django.utils.timezone import utc
from time import time
import HTMLParser, grequests, urllib2, re

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from BHP import settings

from hockeypool.models import *
from match.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

#Define all fantasy point values

cat_vals = {
		'goals' 		: 10,
		'assists' 		: 10,
		'plus_minus' 		: 7,
		'ppg' 			: 7,
		'shg' 			: 12,
		'ppa' 			: 7,
		'sha' 			: 12,
		'psg' 			: 10,
		'gwg' 			: 10,
		'hits' 			: 1,
		'blocks' 		: 1,
		'giveaways' 		: -1,
		'takeaways' 		: 1,
		'faceoff_win' 		: 1,
		'faceoff_loss' 		: -1,
		'shots' 		: 1,
		'pims' 			: -1,
		'fights' 		: 20,
		'shootout_made' 	: 1,
		'shootout_fail' 	: -1,
		'wins' 			: 15,
		'shutouts' 		: 25,
		'otloss'		: 8,
		'penshot_save' 		: 6,
		'penshot_ga' 		: -3,
		'shootout_save' 	: 1,
		'shootout_ga' 		: -1,
		'saves' 		: 1,
		'goals_against' 	: -7,
	}

class NHLOvernightParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.table = 0
		self.rec = 0
		self.player_data = []
		self.player = []
		self.count = 0

	def handle_starttag(self, tag, attributes):
		if self.table:
			if tag == 'tr':
				self.rec = 1
		if tag == 'tbody':
			self.table = 1
		if self.count == 1:
			for name, value in attributes:
				if name=='href':
					id = value.split('=')
					id = id[1]
					self.player_data.append(id)

	def handle_data(self, data):
		if self.rec:
			self.player_data.append(data)
			self.count = self.count + 1

	def handle_endtag(self, tag):
		if tag == 'tr' and self.rec:
			self.player.append(self.player_data)
			self.rec = 0
			self.player_data = []
			self.count = 0
		if tag == 'tbody':
			self.table = 0
                        
def nightly_update():
	st = time()
	pool = Pool.objects.get(pk=1)
	week = pool.current_week
    	URL1 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASALL&viewName=goals&sort=goals&pg="
    	URL2 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASALL&viewName=assists&sort=assists&pg="
    	URL3 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASALL&viewName=rtssPlayerStats&sort=gamesPlayed&pg="
    	URL4 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASALL&viewName=penalties&sort=goals&pg="
    	URL5 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASALL&viewName=shootouts&sort=goals&pg="
    	URL6 = "http://www.nhl.com/ice/playerstats.htm?season=20142015&gameType=2&position=G&viewName=summary&pg="
    	URL7 = "http://www.nhl.com/ice/playerstats.htm?gameType=2&position=G&season=20142015&sort=shootoutGamesWon&status=A&viewName=shootouts&pg="
    	URL8 = "http://www.nhl.com/ice/playerstats.htm?gameType=2&position=G&season=20142015&sort=penaltyShotsAgainst&status=A&viewName=penaltyShot&pg="
	URL9 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASALL&viewName=timeOnIce&sort=timeOnIce&pg="

    	player_goal_data = []
    	player_assist_data = []
    	player_rt_data = []
    	player_pim_data = []
    	player_shootout_data = []
	player_toi_data = []
    	player_id_data = []
    	goalie_win_data = []
    	goalie_shootout_data = []
    	goalie_penshot_data = []
    	goalie_id_data = []

    	uris1 = []
    	uris2 = []
    	uris3 = []
    	uris4 = []
    	uris5 = []
    	uris6 = []
    	uris7 = []
    	uris8 = []
	uris9 = []

    	for i in range(1,25):
        	uris1.append(URL1 + str(i))
		uris2.append(URL2 + str(i))
		uris3.append(URL3 + str(i))
		uris4.append(URL4 + str(i))
		uris5.append(URL5 + str(i))
		uris9.append(URL9 + str(i))

	for i in range(1,4):
		uris6.append(URL6 + str(i))
		uris7.append(URL7 + str(i))
	   	uris8.append(URL8 + str(i))

    	reqs1 = [ grequests.get(x) for x in uris1 ]
    	reqs2 = [ grequests.get(x) for x in uris2 ]
    	reqs3 = [ grequests.get(x) for x in uris3 ]
    	reqs4 = [ grequests.get(x) for x in uris4 ]
    	reqs5 = [ grequests.get(x) for x in uris5 ]
    	reqs6 = [ grequests.get(x) for x in uris6 ]
    	reqs7 = [ grequests.get(x) for x in uris7 ]
    	reqs8 = [ grequests.get(x) for x in uris8 ]
	reqs9 = [ grequests.get(x) for x in uris9 ]

    	resps1 = grequests.map(reqs1)
    	resps2 = grequests.map(reqs2)
    	resps3 = grequests.map(reqs3)
    	resps4 = grequests.map(reqs4)
    	resps5 = grequests.map(reqs5)
    	resps6 = grequests.map(reqs6)
    	resps7 = grequests.map(reqs7)
    	resps8 = grequests.map(reqs8)
	resps9 = grequests.map(reqs9)

    	for x in resps1:
        	p = NHLOvernightParser()
		p.feed(x.content)

		for y in p.player:
	    		if y not in player_goal_data:
				player_goal_data.append(y)

    	for x in resps2:
        	p = NHLOvernightParser()
        	p.feed(x.content)

        	for y in p.player:
            		if y not in player_assist_data:
           			player_assist_data.append(y)

    	for x in resps3:
        	p = NHLOvernightParser()
        	p.feed(x.content)

        	for y in p.player:
            		if y not in player_rt_data:
                		player_rt_data.append(y)
        			player_id_data.append(y[1])

    	for x in resps4:
        	p = NHLOvernightParser()
        	p.feed(x.content)

        	for y in p.player:
            		if y not in player_pim_data:
                		player_pim_data.append(y)

	for x in resps5:
            	p = NHLOvernightParser()
            	p.feed(x.content)

       		for y in p.player:
            		if y not in player_shootout_data:
                		player_shootout_data.append(y)

    	for x in resps6:
        	p = NHLOvernightParser()
        	p.feed(x.content)

        	for y in p.player:
            		if y not in goalie_win_data:
                		goalie_win_data.append(y)
				goalie_id_data.append(y[1])

    	for x in resps7:
        	p = NHLOvernightParser()
        	p.feed(x.content)

        	for y in p.player:
            		if y not in goalie_shootout_data:
                		goalie_shootout_data.append(y)

    	for x in resps8:
        	p = NHLOvernightParser()
        	p.feed(x.content)
            
        	for y in p.player:
            		if y not in goalie_penshot_data:
                		goalie_penshot_data.append(y)

	for x in resps9:
		p = NHLOvernightParser()
		p.feed(x.content)

		for y in p.player:
			if y not in player_toi_data:
				player_toi_data.append(y)

    	full_player_data = []
    	for a in player_id_data:
		temp_player_data = []
		for b in player_goal_data:
            		if b[1] != a:
				continue
	    		else:
				check_goal_var = 0
				temp_player_data.append(b[1])   #ID
				temp_player_data.append(b[2])   #Name
				temp_team = b[3].split(", ")
				temp_team = temp_team[-1]
				temp_player_data.append(Hockey_Team.objects.get(name=temp_team))        #Team
				temp_player_data.append(b[4])   #Position
				temp_player_data.append(b[5])   #Games
				temp_player_data.append(b[6])   #Goals
				temp_player_data.append(b[7])   #Assists
				temp_player_data.append(b[8])   #Points
				temp_player_data.append(b[9])   #Plus Minus
				temp_player_data.append(b[11])  #PPG
				temp_player_data.append(b[12])  #SHG
				temp_player_data.append(b[15])  #GWG
				temp_player_data.append(b[21])  #PSG
	
		for b in player_assist_data:
		    	if b[1] != a:
				continue
			else:
				temp_player_data.append(b[12])  #PPA
				temp_player_data.append(b[11])  #SHA

		for b in player_rt_data:
			if b[1] != a:
				continue
			else:
				temp_player_data.append(b[6])   #Hits
				temp_player_data.append(b[7])   #Blocks
				temp_player_data.append(b[9])   #Giveaways
				temp_player_data.append(b[10])  #Takeaways
				temp_player_data.append(b[11])  #Faceoff Wins
				temp_player_data.append(b[12])  #Faceoff Losses
				temp_player_data.append(b[16])  #Shots

		for b in player_pim_data:
			if b[1] != a:
				continue
			else:
				temp_player_data.append(b[6])   #PIMs
				temp_player_data.append(b[8])   #Majors

		shootout_check_var = 1

		for b in player_shootout_data:
			if b[1] != a:
				continue
			else:
				shootout_check_var = 0
				temp_player_data.append(b[14])          #Shootout Goals
				temp_player_data.append(str(int(b[13]) - int(b[14])))   #Shootout Misses

		if shootout_check_var:
			temp_player_data.append("0")    #If the player has no shootout attempts, assign them manually to zero
			temp_player_data.append("0")    #As otherwise list out of bounds errors will pop up when saving data

                for b in player_toi_data:
                        if b[1] != a:
                                continue
                        else:
                                temp_player_data.append(b[13])

		full_player_data.append(temp_player_data)

	full_goalie_data = []
	for a in goalie_id_data:
		temp_player_data = []
		for b in goalie_win_data:
			if b[1] != a:
				continue
			else:
	                    temp_player_data.append(b[1])   #ID
                            temp_player_data.append(b[2])   #Name
                            temp_team = b[3].split(", ")
                            temp_team = temp_team[-1]
                            temp_player_data.append(Hockey_Team.objects.get(name=temp_team))        #Team
                            temp_player_data.append("G")   #Position
                            temp_player_data.append(b[5])   #Games
			    temp_player_data.append(b[6])	#Wins
			    temp_player_data.append(b[8])	#OTloss
			    temp_player_data.append(b[14])	#Shutout
			    temp_player_data.append(b[10])	#Goals Against
			    temp_player_data.append(b[12])	#Saves
			    temp_player_data.append(b[15])	#Goals
			    temp_player_data.append(b[16])	#Assists
		            temp_player_data.append(b[17])	#PIMs

		penshot_check_var = 1

		for b in goalie_penshot_data:
			if b[1] != a:
				continue
			else:
				penshot_check_var = 0
				temp_player_data.append(b[7])	#PS GA
				temp_player_data.append(b[8])	#PS Sv

		if penshot_check_var:
			temp_player_data.append("0")
			temp_player_data.append("0")
			
		shootout_check_var = 1

		for b in goalie_shootout_data:
			if b[1] != a:
				continue
			else:
				shootout_check_var = 0
				temp_player_data.append(b[16]) #SO Saves
				temp_player_data.append(b[17]) #SO GA

		if shootout_check_var:
			temp_player_data.append("0")
			temp_player_data.append("0")

		full_goalie_data.append(temp_player_data)

	all_activated_skater_ids = Activated_Team.objects.filter(week_id=week.number).values_list("skater_id", flat="True")
	pool = Pool.objects.get(pk=1)
	current_week = pool.current_week

	for x in full_player_data:
		try:
			for i in range(4,26):
				x[i] = int(x[i])
		except ValueError:
			logger.info("Could not convert")
			logger.info(x)
			continue
		except IndexError:
			logger.info("Index error at index %s" % i)
			logger.info(x)
			continue

	  	if Skater.objects.filter(nhl_id=x[0]).exists():
			s = Skater.objects.select_related().get(nhl_id=x[0])
			player_start = time()
			u_toi_parts = x[26].split(':')
	
			if len(u_toi_parts) != 2:
				logger.info("Error with skater: %s. TOI: %s, full data: %s, length: %s" % (s, u_toi_parts, x, len(x)))
				continue
				
			u_toi_sec = int(u_toi_parts[0])*60 + int(u_toi_parts[1])

			c_toi_sec = s.time_on_ice.split(':')
			c_toi_sec = int(c_toi_sec[0])*60 + int(c_toi_sec[1])

			u_games_played     = x[4] - s.games
			u_goals            = x[5] - s.goals
			u_assists          = x[6] - s.assists
			u_points           = x[7] - s.points
			u_plus_minus       = x[8] - s.plus_minus
			u_ppg              = x[9] - s.ppg
			u_shg              = x[10] - s.shg
			u_gwg              = x[11] - s.gwg
			u_psg              = x[12] - s.psg
			u_ppa              = x[13] - s.ppa
			u_sha              = x[14] - s.sha
			u_hits             = x[15] - s.hits
			u_blocks           = x[16] - s.blocks
			u_giveaways        = x[17] - s.giveaways
			u_takeaways        = x[18] - s.takeaways
			u_faceoff_wins     = x[19] - s.faceoff_win
			u_faceoff_loss     = x[20] - s.faceoff_loss
			u_shots            = x[21] - s.shots
			u_pims             = x[22] - s.pims
			u_fights           = x[23] - s.fights
			u_shootout_goals   = x[24] - s.shootout_made
			u_shootout_miss    = x[25] - s.shootout_fail
			u_toi_sec	   = u_toi_sec - c_toi_sec

			if u_fights > 3:
				continue

			if u_toi_sec >= 1200:
				u_toi_point = 1
			elif u_toi_sec >= 1380:
				u_toi_point = 2
			elif u_toi_sec >= 1560:
				u_toi_point = 3
			elif u_toi_sec >= 1740:
				u_toi_point = 4
			elif u_toi_sec >= 1920:
				u_toi_point = 5
			elif u_toi_sec >= 2100:
				u_toi_point = 6
			else:
				u_toi_point = 0

			goals_cat	= u_goals*cat_vals['goals'] + u_psg*cat_vals['psg'] + u_gwg*cat_vals['gwg']  + u_ppg*cat_vals['ppg'] + u_shg*cat_vals['shg']
			assists_cat	= u_assists*cat_vals['assists'] + u_ppa*cat_vals['ppa'] + u_sha*cat_vals['sha']
			plus_minus_cat	= u_plus_minus*cat_vals['plus_minus']
			goalie_cat	= 0
			off_spec_cat	= u_shots*cat_vals['shots'] + u_faceoff_wins*cat_vals['faceoff_win'] + u_faceoff_loss*cat_vals['faceoff_loss']
			true_grit_cat	= u_blocks*cat_vals['blocks'] + u_hits*cat_vals['hits'] + u_fights*cat_vals['fights'] + u_pims*cat_vals['pims'] + u_takeaways*cat_vals['takeaways'] + u_giveaways*cat_vals['giveaways'] + u_toi_point
			shootout_cat = u_shootout_goals*cat_vals['shootout_made'] + u_shootout_miss*cat_vals['shootout_fail']
			fan_points_cat = goals_cat + assists_cat + shootout_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat
			
			curr_date = datetime.now()
			formed_date = "%s-%s-%s" % (curr_date.year, str(curr_date.month).zfill(2), str(curr_date.day).zfill(2))

			if (goals_cat != 0 or assists_cat != 0 or shootout_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
				logger.info("Updating skater: %s"               % (s.name))
				logger.info("Goals: %s, %s, %s"                 % (u_goals, x[5], s.goals))
				logger.info("Assists: %s, %s, %s"               % (u_assists, x[6], s.assists))
				logger.info("Plus Minus: %s, %s, %s"            % (u_plus_minus, x[7], s.plus_minus))
				logger.info("PPG: %s, %s, %s"                   % (u_ppg, x[9], s.ppg))
				logger.info("PPA: %s, %s, %s"                   % (u_ppa, x[13], s.ppa))
				logger.info("SHG: %s, %s, %s"                   % (u_shg, x[10], s.shg))
				logger.info("SHA: %s, %s, %s"                   % (u_sha, x[14], s.sha))
				logger.info("PSG: %s, %s, %s"                   % (u_psg, x[12], s.psg))
				logger.info("GWG: %s, %s, %s"                   % (u_gwg, x[11], s.gwg))
				logger.info("Hits: %s, %s, %s"                  % (u_hits, x[15], s.hits))
				logger.info("Blocks: %s, %s, %s"                % (u_blocks, x[16], s.blocks))
				logger.info("Giveaways: %s, %s, %s"             % (u_giveaways, x[17], s.giveaways))
				logger.info("Takeaways: %s, %s, %s"             % (u_takeaways, x[18], s.takeaways))
				logger.info("Faceoff Win: %s, %s, %s"           % (u_faceoff_wins, x[19], s.faceoff_win))
				logger.info("Faceoff Loss: %s, %s, %s"          % (u_faceoff_loss, x[20], s.faceoff_loss))
				logger.info("Shots: %s, %s, %s"                 % (u_shots, x[21], s.shots))
				logger.info("PIMs: %s, %s, %s"                  % (u_pims, x[22], s.pims))
				logger.info("Fights: %s, %s, %s"                % (u_fights, x[23], s.fights))
				logger.info("Shootut Goals: %s, %s, %s"          % (u_shootout_goals, x[24], s.shootout_made))
				logger.info("Shootout Misses: %s, %s, %s"       % (u_shootout_miss, x[25], s.shootout_fail))

				if Week_Dates.objects.filter(date=formed_date).exists():
					week = Week_Dates.objects.get(date=formed_date)
					point = Point.objects.create(
									skater = s,
									fantasy_points = fan_points_cat,
									week = current_week,
									goals = goals_cat,
									assists = assists_cat,
									shootout = shootout_cat,
									plus_minus = plus_minus_cat,
									true_grit_special = true_grit_cat,
									offensive_special = off_spec_cat,
									goalie = goalie_cat,
									date = formed_date,
								)
					point.save()
					if s.id in all_activated_skater_ids:
						team = Activated_Team.objects.filter(skater=s).filter(week_id=current_week.number)
						if len(team) == 1:
							team = team[0]
							tp = Team_Point.objects.create(
										point = point,
										player = team.player,
										)
							tp.save()
						else:
							logger.info("More than one Activated Team object for id: %s" % s.id)

			fan_points = x[5]*cat_vals['goals'] + x[6]*cat_vals['assists'] + x[8]*cat_vals['plus_minus'] + x[9]*cat_vals['ppg'] + x[10]*cat_vals['shg'] + x[11]*cat_vals['gwg'] + x[12]*cat_vals['psg'] + x[13]*cat_vals['ppa'] + x[14]*cat_vals['sha'] + x[15]*cat_vals['hits'] + x[16]*cat_vals['blocks'] + x[17]*cat_vals['giveaways'] + x[18]*cat_vals['takeaways'] + x[19]*cat_vals['faceoff_win'] + x[20]*cat_vals['faceoff_loss'] + x[21]*cat_vals['shots'] + x[22]*cat_vals['pims'] + x[23]*cat_vals['fights'] + x[24]*cat_vals['shootout_made'] + x[25]*cat_vals['shootout_fail'] + u_toi_point

			s.games 	= x[4]
			s.goals 	= x[5]
			s.assists 	= x[6]
			s.points 	= x[7]
			s.plus_minus 	= x[8]
			s.ppg 		= x[9]
			s.shg 		= x[10]
			s.gwg 		= x[11]
			s.psg 		= x[12]
			s.ppa 		= x[13]
			s.sha 		= x[14]
			s.hits 		= x[15]
			s.blocks 	= x[16]
			s.giveaways 	= x[17]
			s.takeaways 	= x[18]
			s.faceoff_win 	= x[19]
			s.faceoff_loss 	= x[20]
			s.shots 	= x[21]
			s.pims 		= x[22]
			s.fights 	= x[23]
			s.shootout_made = x[24]
			s.shootout_fail = x[25]
			s.time_on_ice = x[26]
			s.fantasy_points = fan_points
			s.save()
		else:
                        u_toi_parts = x[26].split(':')
                        u_toi_sec = int(u_toi_parts[0])*60 + int(u_toi_parts[1])

                        if u_toi_sec >= 1200:
                                u_toi_point = 1
                        elif u_toi_sec >= 1380:
                                u_toi_point = 2
                        elif u_toi_sec >= 1560:
                                u_toi_point = 3
                        elif u_toi_sec >= 1740:
                                u_toi_point = 4
                        elif u_toi_sec >= 1920:
                                u_toi_point = 5
                        elif u_toi_sec >= 2100:
                                u_toi_point = 6
                        else:
                                u_toi_point = 0

			fan_points = x[5]*cat_vals['goals'] + x[6]*cat_vals['assists'] + x[8]*cat_vals['plus_minus'] + x[9]*cat_vals['ppg'] + x[10]*cat_vals['shg'] + x[11]*cat_vals['gwg'] + x[12]*cat_vals['psg'] + x[13]*cat_vals['ppa'] + x[14]*cat_vals['sha'] + x[15]*cat_vals['hits'] + x[16]*cat_vals['blocks'] + x[17]*cat_vals['giveaways'] + x[18]*cat_vals['takeaways'] + x[19]*cat_vals['faceoff_win'] + x[20]*cat_vals['faceoff_loss'] + x[21]*cat_vals['shots'] + x[22]*cat_vals['pims'] + x[23]*cat_vals['fights'] + x[24]*cat_vals['shootout_made'] + x[25]*cat_vals['shootout_fail'] + u_toi_point

			p = Skater(
				nhl_id        = x[0],
				name          = x[1],
				hockey_team   = x[2],
				position      = x[3],
				games         = x[4],
				goals         = x[5],
				assists       = x[6],
				points        = x[7],
				plus_minus    = x[8],
				ppg           = x[9],
				shg           = x[10],
				gwg           = x[11],
				psg           = x[12],
				ppa           = x[13],
				sha           = x[14],
				hits          = x[15],
				blocks        = x[16],
				giveaways     = x[17],
				takeaways     = x[18],
				faceoff_win   = x[19],
				faceoff_loss  = x[20],
				shots         = x[21],
				pims          = x[22],
				fights        = x[23],
				shootout_made = x[24],
				shootout_fail = x[25],
				time_on_ice    = x[26],
				fantasy_points = fan_points,
			)
			p.save()

            		u_games_played     = x[4]
            		u_goals            = x[5]
            		u_assists          = x[6]
			u_points           = x[7]
			u_plus_minus       = x[8]
			u_ppg              = x[9]
			u_shg              = x[10]
			u_gwg              = x[11]
			u_psg              = x[12]
			u_ppa              = x[13]
			u_sha              = x[14]
			u_hits             = x[15]
			u_blocks           = x[16]
			u_giveaways        = x[17]
			u_takeaways        = x[18]
			u_faceoff_wins     = x[19]
			u_faceoff_loss     = x[20]
			u_shots            = x[21]
			u_pims             = x[22]
			u_fights           = x[23]
			u_shootout_goals   = x[24]
			u_shootout_miss    = x[25]

			goals_cat       = u_goals*cat_vals['goals'] + u_psg*cat_vals['psg'] + u_gwg*cat_vals['gwg'] + u_ppg*cat_vals['ppg'] + u_shg*cat_vals['shg']
			assists_cat     = u_assists*cat_vals['assists'] + u_ppa*cat_vals['ppa'] + u_sha*cat_vals['sha']
			plus_minus_cat  = u_plus_minus*cat_vals['plus_minus']
			goalie_cat      = 0
			shootout_cat 	= u_shootout_goals*cat_vals['shootout_made'] + u_shootout_miss*cat_vals['shootout_fail']
			off_spec_cat    = u_shots*cat_vals['shots'] + u_faceoff_wins*cat_vals['faceoff_win'] + u_faceoff_loss*cat_vals['faceoff_loss']
			true_grit_cat   = u_blocks*cat_vals['blocks'] + u_hits*cat_vals['hits'] + u_fights*cat_vals['fights'] + u_pims*cat_vals['pims'] + u_takeaways*cat_vals['takeaways'] + u_giveaways*cat_vals['giveaways'] + u_toi_point
			fan_points_cat = goals_cat + assists_cat + shootout_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat

                        curr_date = datetime.now() - timedelta(days = 1)
                        formed_date = "%s-%s-%s" % (curr_date.year, str(curr_date.month).zfill(2), str(curr_date.day).zfill(2))

                        if (goals_cat != 0 or assists_cat != 0 or shootout_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
                                if Week_Dates.objects.filter(date=formed_date).exists():
                                        week = Week_Dates.objects.get(date=formed_date)
					point = Point.objects.create(
								     skater = p,
								     fantasy_points = fan_points_cat,
								     week = current_week,
								     goals = goals_cat,
								     assists = assists_cat,
								     shootout = shootout_cat,
								     plus_minus = plus_minus_cat,
								     true_grit_special = true_grit_cat,
								     offensive_special = off_spec_cat,
								     goalie = goalie_cat,
								     date = formed_date,
								    )
					point.save()
					if s.id in all_activated_skater_ids:
                                                team = Activated_Team.objects.filter(skater=s).filter(week_id=current_week.number)
                                                if len(team) == 1:
                                                        team = team[0]
                                                        tp = Team_Point.objects.create(
                                                                                point = point,
                                                                                player = team.player,
                                                                                )
                                                        tp.save()
                                                else:
                                                        logger.info("More than one Activated Team object for id: %s" % s.id)

        logger.info(full_goalie_data)
	for x in full_goalie_data:
		try:
			for i in range(4, 17):
				x[i] = int(x[i])

			if Skater.objects.filter(nhl_id=x[0]).exists():
				s = Skater.objects.select_related().get(nhl_id=x[0])
				u_goals		= x[10] - s.goals
				u_assists	= x[11] - s.assists
				u_pims		= x[12] - s.pims 
				u_wins		= x[5] - s.wins
				u_otloss	= x[6] - s.otloss
				u_shutouts	= x[7] - s.shutouts
				u_penshot_save	= x[14] - s.penshot_save
				u_penshot_ga	= x[13] - s.penshot_ga
				u_shootout_save = x[15] - s.shootout_save
				u_shootout_ga	= x[16] - s.shootout_ga
				u_saves		= x[9] - s.saves
				u_goals_against = x[8] - s.goals_against

				goals_cat = u_goals*cat_vals['goals']
				assists_cat = u_assists*cat_vals['assists']
				shootout_cat = u_shootout_save*cat_vals['shootout_save'] + u_shootout_ga*cat_vals['shootout_ga']
				plus_minus_cat = 0
				true_grit_cat = u_pims*cat_vals['pims']
				off_spec_cat = 0
				goalie_cat = u_wins*cat_vals['wins'] + u_otloss*cat_vals['otloss'] + u_shutouts*cat_vals['shutouts'] + u_penshot_save*cat_vals['penshot_save'] + u_penshot_ga*cat_vals['penshot_ga'] + u_saves*cat_vals['saves'] + u_goals_against*cat_vals['goals_against']
				fan_points_cat = goals_cat + assists_cat + shootout_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat
				curr_date = datetime.now() - timedelta(days = 1)
				formed_date = "%s-%s-%s" % (curr_date.year, str(curr_date.month).zfill(2), str(curr_date.day).zfill(2))

				if (goals_cat != 0 or assists_cat != 0 or shootout_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
					logger.info("Processing existing goalie: %s" % s.name)
					logger.info("Goals: %s, %s, %s"         % (u_goals,             x[10],  s.goals))
					logger.info("Assists: %s, %s, %s"       % (u_assists,           x[11],  s.assists))
					logger.info("PIMs: %s, %s, %s"          % (u_pims,              x[12],  s.pims))
					logger.info("Wins: %s, %s, %s"          % (u_wins,              x[5],   s.wins))
					logger.info("OT Loss: %s, %s, %s"       % (u_otloss,            x[6],   s.otloss))
					logger.info("Shutouts: %s, %s, %s"      % (u_shutouts,          x[7],   s.shutouts))
					logger.info("Penshot Save: %s, %s, %s"  % (u_penshot_save,      x[14],  s.penshot_save))
					logger.info("Penshot GA: %s, %s, %s"    % (u_penshot_ga,        x[13],  s.penshot_ga))
					logger.info("Shootout Save: %s, %s, %s" % (u_shootout_save,     x[15],  s.shootout_save))
					logger.info("Shootout GA: %s, %s, %s"   % (u_shootout_ga,       x[15],  s.shootout_ga))
					logger.info("Saves: %s, %s, %s"         % (u_saves,             x[9],   s.saves))
					logger.info("Goals Against: %s, %s, %s" % (u_goals_against,     x[8],   s.goals_against))
					if Week_Dates.objects.filter(date=formed_date).exists():
						week = Week_Dates.objects.get(date=formed_date)
						point = Point.objects.create(
										skater = s,
										week = current_week,
										fantasy_points = fan_points_cat,
										goals = goals_cat,
										assists = assists_cat,
										shootout = shootout_cat,
										plus_minus = plus_minus_cat,
										true_grit_special = true_grit_cat,
										offensive_special = off_spec_cat,
										goalie = goalie_cat,
										date = formed_date,
									)
						logger.info(point.id)
						point.save()
						if s.id in all_activated_skater_ids:
							team = Activated_Team.objects.filter(skater=s).filter(week_id=current_week.number)
							if len(team) == 1:
								team = team[0]
								tp = Team_Point.objects.create(
											point = point,
											player = team.player,
											)
								tp.save()
							else:
								logger.info("More than one Activated Team object for id: %s" % s.id)

				fan_points = x[10]*cat_vals['goals'] + x[11]*cat_vals['assists'] + x[12]*cat_vals['pims'] + x[5]*cat_vals['wins'] + x[6]*cat_vals['otloss'] + x[7]*cat_vals['shutouts'] + x[14]*cat_vals['penshot_save'] + x[13]*cat_vals['penshot_ga'] + x[15]*cat_vals['shootout_save'] + x[16]*cat_vals['shootout_ga'] + x[9]*cat_vals['saves'] + x[8]*cat_vals['goals_against']
		
				s.games         = x[4]
				s.goals         = x[10]
				s.assists       = x[11]
				s.points        = x[10] + x[11]
				s.pims          = x[12]
				s.wins          = x[5]
				s.otloss        = x[6]
				s.shutouts      = x[7]
				s.penshot_save  = x[14]
				s.penshot_ga    = x[13]
				s.shootout_save = x[15]
				s.shootout_ga   = x[16]
				s.saves         = x[9]
				s.goals_against = x[8]
				s.fantasy_points = fan_points
				s.save()
			else:
				logger.info("Processing new goalie")
				u_goals         = x[10]
				u_assists       = x[11]
				u_pims          = x[12]
				u_wins          = x[5]
				u_otloss        = x[6] 
				u_shutouts      = x[7] 
				u_penshot_save  = x[14]
				u_penshot_ga    = x[13] 
				u_shootout_save = x[15] 
				u_shootout_ga   = x[16]
				u_saves         = x[9]
				u_goals_against = x[8]

				fan_points = u_goals*cat_vals['goals'] + u_assists*cat_vals['assists'] + u_pims*cat_vals['assists'] + u_wins*cat_vals['wins'] + u_otloss*cat_vals['otloss'] + u_shutouts*cat_vals['shutouts'] + u_penshot_save*cat_vals['penshot_save'] + u_penshot_ga*cat_vals['penshot_ga'] + u_shootout_save*cat_vals['shootout_save'] + u_shootout_ga*cat_vals['shootout_ga'] + u_saves*cat_vals['saves'] + u_goals_against*cat_vals['goals_against']

				s = Skater(
					nhl_id        = x[0],
					name          = x[1],
					hockey_team   = x[2],
					position      = x[3],
					games         = x[4],
					goals         = x[10],
					assists       = x[11],
					points        = x[10] + x[11],
					pims          = x[12],
					wins          = x[5],
					otloss        = x[6],
					shutouts      = x[7],
					penshot_save  = x[14],
					penshot_ga    = x[13],
					shootout_save = x[15],
					shootout_ga   = x[16],
					saves         = x[9],
					goals_against = x[8],
					fantasy_points = fan_points,
					)
				s.save()
				logger.info("Processed: %s" % s.name)

				goals_cat = u_goals*cat_vals['goals']
				assists_cat = u_assists*cat_vals['assists']
				shootout_cat = u_shootout_save*cat_vals['shootout_save'] + u_shootout_ga*cat_vals['shootout_ga']
				plus_minus_cat = 0
				true_grit_cat = u_pims*cat_vals['pims']
				off_spec_cat = 0
				goalie_cat = u_wins*cat_vals['wins'] + u_otloss*cat_vals['otloss'] + u_shutouts*cat_vals['shutouts'] + u_penshot_save*cat_vals['penshot_save'] + u_penshot_ga*cat_vals['penshot_ga'] +u_saves*cat_vals['saves'] + u_goals_against*cat_vals['goals_against']
				fan_points_cat = goals_cat + assists_cat + shootout_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat

				curr_date = datetime.now() - timedelta(days = 1)
				formed_date = "%s-%s-%s" % (curr_date.year, str(curr_date.month).zfill(2), str(curr_date.day).zfill(2))
				logger.info(goals_cat, assists_cat, shootout_cat, plus_minus_cat, true_grit_cat, off_spec_cat, goalie_cat, fan_points_cat)

				if (goals_cat != 0 or assists_cat != 0 or shootout_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
					point = Point.objects.create(
							     skater = s,
							     week = current_week,
							     fantasy_points = fan_points_cat,
							     goals = goals_cat,
							     assists = assists_cat,
							     shootout = shootout_cat,
							     plus_minus = plus_minus_cat,
							     true_grit_special = true_grit_cat,
							     offensive_special = off_spec_cat,
							     goalie = goalie_cat,
							     date = formed_date,
							    )
					logger.info(point.id)
					point.save()
					if s.id in all_activated_skater_ids:
                                                team = Activated_Team.objects.filter(skater=s).filter(week_id=current_week.number)
                                                if len(team) == 1:
                                                        team = team[0]
                                                        tp = Team_Point.objects.create(
                                                                                point = point,
                                                                                player = team.player,
                                                                                )
                                                        tp.save()
                                                else:
                                                        logger.info("More than one Activated Team object for id: %s" % s.id)

		except:
			print x

	diff_time = time() - st
	logger.info("Total time elapsed: %s" % diff_time)

logger.info("Starting player updates")
nightly_update()
logger.info("Player updates finished")
