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

#Define all fantasy point values

cat_vals = {
		'goals' 	: 10,
		'assists' 	: 10,
		'plus_minus' 	: 7,
		'ppg' 		: 10,
		'shg' 		: 10,
		'ppa' 		: 10,
		'sha' 		: 10,
		'psg' 		: 10,
		'gwg' 		: 10,
		'hits' 		: 1,
		'blocks' 	: 1,
		'giveaways' 	: -1,
		'takeaways' 	: 1,
		'faceoff_win' 	: 1,
		'faceoff_loss' 	: -1,
		'shots' 	: 1,
		'pims' 		: -2,
		'fights' 	: 30,
		'shootout_made' : 3,
		'shootout_fail' : -2,
		'wins' 		: 15,
		'shutouts' 	: 25,
		'otloss'	: 8,
		'penshot_save' 	: 6,
		'penshot_ga' 	: -3,
		'shootout_save' : 3,
		'shootout_ga' 	: -3,
		'saves' 	: 1,
		'goals_against' : -7,
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

class NHLRealtimeParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)

	def handle_startteg(self, tag, attributes):
		print "1"

	def hendle_date(self, date):
		print "2"

	def hand_endtag(self, tag):
		print "3"

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

def turn_end(draft_picks):
	logger.info("Ending draft turn")
	count = 0
	for x in draft_picks:
		if x.pick == None:
			break
		else:
			count = count + 1
	if count == 0:
		return
	else:
		prev_pick = draft_picks[count - 1]
		curr_pick = draft_picks[count]
		curr_time = datetime.utcnow().replace(tzinfo=utc)

		if Draft_Swap.objects.filter(pick = draft_picks[count]).exists():
			prev_swap = Draft_Swap.objects.filter(pick = draft_picks[count]).order_by("-id")[0]
			prev_time = prev_swap.time
			print prev_time
		else:
			prev_time = prev_pick.time

		diff_time = curr_time - prev_time

		if diff_time.total_seconds() > 120:
			logger.info("Swapping picks")
			current_round = curr_pick.round
			round_picks = Draft_Pick.objects.filter(round_id = current_round.id)
			total_picks = len(round_picks)
			not_made_picks = 0

			logger.info("Round picks pre-swap:")
			for x in round_picks:
				logger.info("%s" % x.player)
				if x.pick == None:
					not_made_picks = not_made_picks + 1

			start_index = total_picks - not_made_picks
			temp_draft_pick = Draft_Pick.objects.filter(id=round_picks[start_index].id) 
			temp_draft_pick = temp_draft_pick[0]
			i = start_index

			while(i < total_picks - 1):
				round_picks[i].player = round_picks[i+1].player
				round_picks[i].save()
				i = i + 1

			round_picks[len(round_picks) - 1].player = temp_draft_pick.player
			round_picks[len(round_picks) - 1].save()
			draft_swap = Draft_Swap.objects.create(round = current_round, time = datetime.now(), pick = round_picks[start_index])
			draft_swap.save()

			round_picks = Draft_Pick.objects.filter(round_id = current_round.id)

                        logger.info("Round picks post-swap:")
                        for x in round_picks:
                                logger.info("%s" % x.player)
	return

def end_draft():
	logger.info("Ending the draft")
	picks = Draft_Pick.objects.all()
	for p in picks:
		t = Team.objects.create(skater = p.pick, player = p.player, week=1, active=0)
		t.save()


def real_time_update():
	logger.info("Real time updating")

def nightly_update():
	logger.info("Nightly update")
	URL1 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20132ALLSASALL&viewName=goals&sort=goals&pg="
	URL2 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20132ALLSASALL&viewName=assists&sort=assists&pg="
	URL3 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20132ALLSASALL&viewName=rtssPlayerStats&sort=gamesPlayed&pg="
	URL4 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20132ALLSASALL&viewName=penalties&sort=goals&pg="
	URL5 = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20132ALLSASALL&viewName=shootouts&sort=goals&pg="
        URL6 = "http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&position=G&viewName=summary&pg="
        URL7 = "http://www.nhl.com/ice/playerstats.htm?gameType=2&position=G&season=20122013&sort=shootoutGamesWon&status=A&viewName=shootouts&pg="
        URL8 = "http://www.nhl.com/ice/playerstats.htm?gameType=2&position=G&season=20122013&sort=penaltyShotsAgainst&status=A&viewName=penaltyShot&pg="

	player_goal_data = []
	player_assist_data = []
	player_rt_data = []
	player_pim_data = []
	player_shootout_data = []
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

	for i in range(1,30):
		uris1.append(URL1 + str(i))
		uris2.append(URL2 + str(i))
		uris3.append(URL3 + str(i))
		uris4.append(URL4 + str(i))
		uris5.append(URL5 + str(i))

	for i in range(1,5):
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

	resps1 = grequests.map(reqs1)
        resps2 = grequests.map(reqs2)
        resps3 = grequests.map(reqs3)
        resps4 = grequests.map(reqs4)
        resps5 = grequests.map(reqs5)
        resps6 = grequests.map(reqs6)
        resps7 = grequests.map(reqs7)
        resps8 = grequests.map(reqs8)
	
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
			temp_player_data.append("0")            #If the player has no shootout attempts, assign them manually to zero
			temp_player_data.append("0")            #As otherwise list out of bounds errors will pop up when saving data

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

	for x in full_player_data:
                for i in range(4,26):
                        x[i] = int(x[i])

		if Skater.objects.filter(nhl_id=x[0]).exists():
			s = Skater.objects.get(nhl_id=x[0])
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

			goals_cat	= u_goals*cat_vals['goals'] + u_psg*cat_vals['psg'] + u_gwg*cat_vals['gwg']
			assists_cat	= u_assists*cat_vals['assists']
			spec_team_cat	= u_ppg*cat_vals['ppg'] + u_ppa*cat_vals['ppa'] + u_shg*cat_vals['shg'] + u_sha*cat_vals['sha']
			plus_minus_cat	= u_plus_minus*cat_vals['plus_minus']
			goalie_cat	= 0
			off_spec_cat	= u_shootout_goals*cat_vals['shootout_made'] + u_shootout_miss*cat_vals['shootout_fail'] + u_shots*cat_vals['shots'] + u_faceoff_wins*cat_vals['faceoff_win'] + u_faceoff_loss*cat_vals['faceoff_loss']
			true_grit_cat	= u_blocks*cat_vals['blocks'] + u_hits*cat_vals['hits'] + u_fights*cat_vals['fights'] + u_pims*cat_vals['pims'] + u_takeaways*cat_vals['takeaways'] + u_giveaways*cat_vals['giveaways']
			fan_points_cat = goals_cat + assists_cat + spec_team_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat

			curr_date = datetime.now()
			formed_date = "%s-%s-%s" % (curr_date.year, str(curr_date.month).zfill(2), str(curr_date.day).zfill(2))

			if (goals_cat != 0 or assists_cat != 0 or spec_team_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
				if Week_Dates.objects.filter(date=formed_date).exists():
					week = Week_Dates.objects.filter(date=formed_date)
					point = Point.objects.create(
									skater = s,
									fantasy_points = fan_points_cat,
									week = week.week,
									goals = goals_cat,
									assists = assists_cat,
									special_teams = spec_team_cat,
									plus_minus = plus_minus_cat,
									true_grit_special = true_grit_cat,
									offensive_special = off_spec_cat,
									goalie = goalie_cat,
									date = formed_date,
								)
					point.save()

			fan_points = x[5]*cat_vals['goals'] + x[6]*cat_vals['assists'] + x[8]*cat_vals['plus_minus'] + x[9]*cat_vals['ppg'] + x[10]*cat_vals['shg'] + x[11]*cat_vals['gwg'] + x[12]*cat_vals['psg'] + x[13]*cat_vals['ppa'] + x[14]*cat_vals['sha'] + x[15]*cat_vals['hits'] + x[16]*cat_vals['blocks'] + x[17]*cat_vals['giveaways'] + x[18]*cat_vals['takeaways'] + x[19]*cat_vals['faceoff_win'] + x[20]*cat_vals['faceoff_loss'] + x[21]*cat_vals['shots'] + x[22]*cat_vals['pims'] + x[23]*cat_vals['fights'] + x[24]*cat_vals['shootout_made'] + x[25]*cat_vals['shootout_fail']

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
			s.shottout_fail = x[25]
			s.fantasy_points = fan_points
			s.save()
		else:
			fan_points = x[5]*cat_vals['goals'] + x[6]*cat_vals['assists'] + x[8]*cat_vals['plus_minus'] + x[9]*cat_vals['ppg'] + x[10]*cat_vals['shg'] + x[11]*cat_vals['gwg'] + x[12]*cat_vals['psg'] + x[13]*cat_vals['ppa'] + x[14]*cat_vals['sha'] + x[15]*cat_vals['hits'] + x[16]*cat_vals['blocks'] + x[17]*cat_vals['giveaways'] + x[18]*cat_vals['takeaways'] + x[19]*cat_vals['faceoff_win'] + x[20]*cat_vals['faceoff_loss'] + x[21]*cat_vals['shots'] + x[22]*cat_vals['pims'] + x[23]*cat_vals['fights'] + x[24]*cat_vals['shootout_made'] + x[25]*cat_vals['shootout_fail']

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
				fantasy_poionts = fan_points,
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

                        goals_cat       = u_goals*cat_vals['goals'] + u_psg*cat_vals['psg'] + u_gwg*cat_vals['gwg']
                        assists_cat     = u_assists*cat_vals['assists']
                        spec_team_cat   = u_ppg*cat_vals['ppg'] + u_ppa*cat_vals['ppa'] + u_shg*cat_vals['shg'] + u_sha*cat_vals['sha']
                        plus_minus_cat  = u_plus_minus*cat_vals['plus_minus']
                        goalie_cat      = 0
                        off_spec_cat    = u_shootout_goals*cat_vals['shootout_made'] + u_shootout_miss*cat_vals['shootout_fail'] + u_shots*cat_vals['shots'] + u_faceoff_wins*cat_vals['faceoff_win'] + u_faceoff_loss*cat_vals['faceoff_loss']
                        true_grit_cat   = u_blocks*cat_vals['blocks'] + u_hits*cat_vals['hits'] + u_fights*cat_vals['fights'] + u_pims*cat_vals['pims'] + u_takeaways*cat_vals['takeaways'] + u_giveaways*cat_vals['giveaways']
                        fan_points_cat = goals_cat + assists_cat + spec_team_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat

			if (goals_cat != 0 or assists_cat != 0 or spec_team_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
                                point = Point.objects.create(
                                                                skater = s,
                                                                fantasy_points = fan_points_cat,
                                                                goals = goals_cat,
                                                                assists = assists_cat,
                                                                special_teams = spec_team_cat,
                                                                plus_minus = plus_minus_cat,
                                                                true_grit_special = true_grit_cat,
                                                                offensive_special = off_spec_cat,
                                                                goalie = goalie_cat,
                                                                date = formed_date,
                                                        )
                                point.save()

	for x in full_goalie_data:
		for i in range(4, 17):
			x[i] = int(x[i])

		if Skater.objects.filter(nhl_id=x[0]).exists():
			s = Skater.objects.get(nhl_id=x[0])
			u_goals		= x[10] - s.goals
			u_assists	= x[11] - s.assists
			u_pims		= x[12] - s.pims 
			u_wins		= x[5] - s.wins
			u_otloss	= x[6] - s.otloss
			u_shutouts	= x[7] - s.shutouts
			u_penshot_save	= x[15] - s.penshot_save
			u_penshot_ga	= x[16] - s.penshot_ga
			u_shootout_save = x[14] - s.shootout_save
			u_shootout_ga	= x[13] - s.shootout_ga
			u_saves		= x[9] - s.saves
			u_goals_against = x[8] - s.goals_against

			goals_cat = u_goals*cat_vals['goals']
			assists_cat = u_assists*cat_vals['assists']
			spec_teams_cat = 0
			plus_minus_cat = 0
			true_grit_cat = u_pims*cat_vals['pims']
			off_spec_cat = 0
			goalie_cat = u_wins*cat_vals['wins'] + u_otloss*cat_vals['otloss'] + u_shutouts*cat_vals['shutouts'] + u_penshot_save*cat_vals['penshot_save'] + u_penshot_ga*cat_vals['penshot_ga'] + u_shootout_save*cat_vals['shootout_save'] + u_shootout_ga*cat_vals['shootout_ga'] + u_saves*cat_vals['saves'] + u_goals_against*cat_vals['goals_against']
                        fan_points_cat = goals_cat + assists_cat + spec_team_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat
                        curr_date = datetime.now()
                        formed_date = "%s-%s-%s" % (curr_date.year, str(curr_date.month).zfill(2), str(curr_date.day).zfill(2))

                        if (goals_cat != 0 or assists_cat != 0 or spec_team_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
				if Week_Dates.objects.filter(date=formed_date).exists():
					week = Week_Dates.objects.filter(date=formed_date)
					point = Point.objects.create(
									skater = s,
									week = week.week,
									fantasy_points = fan_points_cat,
									goals = goals_cat,
									assists = assists_cat,
									special_teams = spec_team_cat,
									plus_minus = plus_minus_cat,
									true_grit_special = true_grit_cat,
									offensive_special = off_spec_cat,
									goalie = goalie_cat,
									date = formed_date,
								)
					point.save()

			fan_points = x[10]*cat_vals['goals'] + x[11]*cat_vals['assists'] + x[12]*cat_vals['assists'] + x[5]*cat_vals['wins'] + x[6]*cat_vals['otloss'] + x[7]*cat_vals['shutouts'] + x[14]*cat_vals['penshot_save'] + x[13]*cat_vals['penshot_ga'] + x[15]*cat_vals['shootout_save'] + x[16]*cat_vals['shootout_ga'] + x[9]*cat_vals['saves'] + x[8]*cat_vals['goals_against']
	
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
                        u_goals         = x[10]
                        u_assists       = x[11]
                        u_pims          = x[12]
                        u_wins          = x[5]
                        u_otloss        = x[6] 
                        u_shutouts      = x[7] 
                        u_penshot_save  = x[15]
                        u_penshot_ga    = x[16] 
                        u_shootout_save = x[14] 
                        u_shootout_ga   = x[13]
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

                        goals_cat = u_goals*cat_vals['goals']
                        assists_cat = u_assists*cat_vals['assists']
                        spec_teams_cat = 0
                        plus_minus_cat = 0
                        true_grit_cat = u_pims*cat_vals['pims']
                        off_spec_cat = 0
                        goalie_cat = u_wins*cat_vals['wins'] + u_otloss*cat_vals['otloss'] + u_shutouts*cat_vals['shutouts'] + u_penshot_save*cat_vals['penshot_save'] + u_penshot_ga*cat_vals['penshot_ga'] + u_shootout_save*cat_vals['shootout_save'] + u_shootout_ga*cat_vals['shootout_ga'] + u_saves*cat_vals['saves'] + u_goals_against*cat_vals['goals_against']
                        fan_points_cat = goals_cat + assists_cat + spec_team_cat + plus_minus_cat + goalie_cat + off_spec_cat + true_grit_cat
                        curr_date = datetime.now()
                        formed_date = "%s-%s-%s" % (curr_date.year, str(curr_date.month).zfill(2), str(curr_date.day).zfill(2))

                        if (goals_cat != 0 or assists_cat != 0 or spec_team_cat != 0 or true_grit_cat != 0 or plus_minus_cat != 0 or goalie_cat != 0 or off_spec_cat != 0):
                                point = Point.objects.create(
                                                                skater = s,
                                                                fantasy_points = fan_points_cat,
                                                                goals = goals_cat,
                                                                assists = assists_cat,
                                                                special_teams = spec_team_cat,
                                                                plus_minus = plus_minus_cat,
                                                                true_grit_special = true_grit_cat,
                                                                offensive_special = off_spec_cat,
                                                                goalie = goalie_cat,
                                                                date = formed_date,
                                                        )
                                point.save()

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

def activate_players(week):
        logger.info("Activating players")
        Team.objects.all().update(active = 0)
	a = Activation.objects.filter(week__number = week.number)
	for x in a:
		logger.info("Processing activationg: %s for player: %s" % (a.skater, a.player))
		Team.objects.filter(skater = a.skater).update(active=1)

        logger.info("Activations processed")
        return

def match_end(match):
        logger.info("Ending match: %s" % x)

def week_end():
	current_time = datetime.utcnow()
	td = timedelta(days = 1)
	yester_time = current_time - td

	if current_time.year >= 2013 and current_time.month >= 10:
		formed_date = "%s-%s-%s" % (current_time.year, str(current_time.month).zfill(2), str(current_time.day).zfill(2))
		yester_date = "%s-%s-%s" % (yester_time.year, str(yester_time.month).zfill(2), str(yester_time.day).zfill(2))
		current_week = Week_Dates.objects.filter(date=formed_date)

		if current_week == None:
			current_week = 0
		else:
			current_week = current_week.number

		yester_week = Week_Dates.objects.filter(date=yester_date)
		if yester_week == None:
			yester_week = 0
		else:
			yester_week = yester_week.number

		if current_week.number == yester_week:
			logger.info("Not a week end yet")
		else:
			p = Player.objects.all()
			for x in p:
				logger.info("Processing activations for: %s" % x.name)
				a = Activation.objects.select_related().filter(player = x)
				for y in a:
					logger.info(a.skater.name)
					activated = Activated_Team.objects.create(skater = a.skater, player = x)
					activated.save()
	else:
		logger.info("Not october yet... season hasn't started")
		return

	if yester_week != 0:
		if current_week.week.number != yester_week.week.number:
			activate_players(current_week.week)
			m = Matches.objects.all(week = yester_week.week)
			for x in m:
				match_end(x)
	else:
		if current_week.week.number == 1:
			activate_players(current_week.week)

	logger.info("Week ended")

draft_pick_count = Draft_Pick.objects.all().count()
draft_over = 0
current_time = datetime.utcnow()
logger.info(current_time)
formed_date = "%s-%s-%s" % (current_time.year, str(current_time.month).zfill(2), str(current_time.day).zfill(2))

if current_time.month < 10 and current_time.year == 2014:
	formed_date = "2014-10-01"

week = Week_Dates.objects.get(date=formed_date)
week = week.week

if draft_pick_count == 0:
	logger.info("No draft picks. Checking ready status")
	draft_end_count = Draft_Start.objects.filter(status=0).count()
	if draft_end_count == 0:
		logger.info("Draft ready to start. Commencing cleanup shit.")
	else:
		logger.info("Draft not ready to start")
else:
	draft_picks = Draft_Pick.objects.all()
	draft_end_check = 0
	for x in draft_picks:
		if x.pick == None:
			draft_end_check = 1
			turn_end(draft_picks)
			break
	if draft_end_check == 1:
		logger.info("Draft not over")
	else:
		t = Team.objects.all().count()
		if t > 0:
			draft_over = 1
		else:
			end_draft()

if draft_over == 1:
	if current_time.minute % 15 == 0:
		real_time_update()
	if current_time.hour == 10 and current_time.minute % 60 == 0:
		logger.info("Running nightly updates")
		nightly_update()
		injury_update()
	if current_time.hour == 0 and current_time.minute == 1:
		logger.info("Running weekly updates")
		week_end()

