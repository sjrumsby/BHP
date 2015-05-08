from urllib2 import urlopen
from parsers import *
import os
import re
import sys
import traceback
import vars

class Game():
	
	def __init__(self, season, game, year):
		self.seasonID = season
		self.gameID = game
		self.yearID = year
		self.homeTeamSkaters = {}
		self.awayTeamSkaters = {}
		self.parseGame()

	def makeSkater(self, s):
		return {
					"nhl_id" : s, 
					"shots" : 0, 
					"blocks" : 0, 
					"giveaways" : 0, 
					"takeaways" : 0, 
					"hits" : 0, 
					"faceoffwins" : 0, 
					"faceofflosses" : 0,
					"goals" : 0,
					"powerplaygoals" : 0,
					"shorthandedgoals" : 0,
					"assists" : 0,
					"powerplayassists" : 0,
					"shorthandedassists" : 0,
					"firststars" : 0,
					"secondstars" : 0,
					"thirdstars" : 0,
					"penaltyshotgoals" : 0,
					"emptynetassists" : 0,
					"emptynetgoals" : 0,
					"gamewinninggoals" : 0,
					"gamewinningassists" : 0,
					"misses" : 0,
					"shootoutmisses" : 0,
					"shootoutgoals" : 0,
					"pims" : 0,
					"pimsdrawn" : 0,
					"blockedshots" : 0,
					"shootoutgoalsagainst" : 0,
					"shootoutsaves" : 0,
					"timeonice" : '',
					"wins" : 0,
					"losses" : 0,
					"otlosses" : 0,
					"shutouts" : 0,
					"penaltyshotgoalsagainst" : 0,
					"penaltyshotsaves" : 0,
					"hitstaken" : 0,
					"goalsagainst" : 0,
					"saves" : 0,
                    "plusminus" : 0,
                    "fights" : 0,
				}

	def pretty(self, d, indent=0):
	   for key, value in d.iteritems():
		  print '\t' * indent + str(key)
		  if isinstance(value, dict):
			 pretty(value, indent+1)
		  else:
			 print '\t\t' * (indent+1) + str(value)

	def print_to_file(self, homeTeamSkaters, awayTeamSkaters):
		fp = "JSON/" + yearID + "/" + gameID + "_home.json"
		f = open(fp, 'w')
		f.write('{ \n')
		for key, value in homeTeamSkaters.iteritems():
			f.write('\t"' + str(key) + '" : ' + '{\n')
			if isinstance(value, dict):
				for key2, value2 in homeTeamSkaters[key].iteritems():
					f.write( '\t\t"' + str(key2) + '" : "' + str(value2) + '",\n')
				f.write( '\t\n},')
		f.write( '}\n')
		
		fp = "JSON/" + yearID + "/" + gameID + "_away.json"
		f = open(fp, 'w')
		f.write('{ \n')
		for key, value in awayTeamSkaters.iteritems():
			f.write('\t"' + str(key) + '" : ' + '{\n')
			if isinstance(value, dict):
				for key2, value2 in awayTeamSkaters[key].iteritems():
					f.write( '\t\t"' + str(key2) + '" : "' + str(value2) + '",\n')
				f.write( '\t\n},')
		f.write( '}\n')
		
	def convertHockeyTeamName(self, team):
		if team == "S.J":
			return "SJS"
		elif team == "N.J":
			return "NJD"
		elif team == "T.B":
			return "TBL"
		elif team == "L.A":
			return "LAK"
		else:
			return team

	def processFaceOff(self, play):
		parts = play.split(" - ")
		winnerTeam = parts[0][0:3].strip()
		parts = parts[1].split(" vs ")
		playerOne = parts[0].split("#")[1][0:2].strip()
		playerOneTeam = parts[0][0:3].strip()
		playerTwo = parts[1].split("#")[1][0:2].strip()
		playerTwoTeam = parts[1][0:3].strip()
		return {"playerOne" : playerOne, "playerOneTeam" : playerOneTeam, "playerTwo" : playerTwo, "playerTwoTeam" : playerTwoTeam, "winnerTeam" : winnerTeam}

	def processBlock(self, play):
		parts = play.split(" BLOCKED BY ")
		shooter = parts[0].split("#")[1][0:2].strip()
		shooter_team = self.convertHockeyTeamName(parts[0].strip()[0:3])
		team = self.convertHockeyTeamName(parts[1].strip()[0:3])
		blocker = parts[1].split("#")[1][0:2].strip()
		return {"player" : blocker, "team" : team, "shooter" : shooter, "shooter_team" : shooter_team}

	def processShot(self, play):
		team = play[0:3]
		parts = play.split('#')
		shooter = parts[1][0:2].strip()
		if "Penalty Shot" in play:
			psg = True
		else:
			psg = False
		return {"player" : shooter, "team" : team, "psg" : psg}
		return {"player" : shooter, "team" : team, "psg" : psg}
		
	def processGiveaway(self, team, play):
		if len(team) < 5:
			parts = play.split("#")
			skater = parts[1][0:2].strip()
		else:
			parts = play.split("#")
			team = parts[0].strip()[0:2].strip()
			skater = parts[1][0:2].strip()
		return {"player" : skater, "team" : team}

	def processTakeaway(self, team, play):
		if len(team) < 5:
			parts = play.split("#")
			skater = parts[1][0:2].strip()
		else:
			parts = play.split("#")
			team = parts[0].strip()[0:2].strip()
			skater = parts[1][0:2].strip()
		return {"player" : skater, "team" : team}

	def processMiss(self, play):
		team = play[0:3]
		parts = play.split("#")
		shooter = parts[1][0:2].strip()
		if "Penalty Shot" in play:
			psg = True
		else:
			psg = False
		return {"player" : shooter, "team" : team, "psg" : psg}

	def processHit(self, play):
		team = play[0:3]
		parts = play.split("#")
		
		if len(parts) == 2:
			hitter = parts[1][0:2].strip()
			receiver = None
		elif len(parts) == 3:
			hitter = parts[1][0:2].strip()
			receiver = parts[2][0:2].strip()
		else:
			print "An unknown error occurrec: %s" % play
		return {"player" : hitter, "team" : team, "receiver" : receiver}

	def processGoal(self, play):
		team = play[0:3]
		parts = play.split("#")
		shooter = parts[1][0:2].strip()
		assistOne = None
		assistTwo = None
		if len(parts) == 3:
			assistOne = parts[2][0:2].strip()
		if len(parts) == 4:
			assistOne = parts[2][0:2].strip()
			assistTwo = parts[3][0:2].strip()
		if "Penalty Shot" in play:
			psg = True
		else:
			psg = False
		return {"team" : team, "shooter"  : shooter, "assistOne" : assistOne, "assistTwo" : assistTwo, "psg" : psg}

	def processPenalty(self, player, penalty):
		team = player[0:3].strip()
		if "TEAM" not in player:
			parts = player.split("#")
			number = parts[1][0:2].strip()
		else:
			number = "Team"
		minutes = re.findall("\((\d+) min\)", penalty)
		
		if minutes:
			minutes = minutes[0]
		else:
			minutes = '2'
			
		if penalty.find("#") != -1:
			parts = penalty.split("#")
			if len(parts) == 2:
				if penalty.find("Served By") != -1:
					drawn_by = None	
				else:
					drawn_by = penalty.split("#")[-1][0:2].strip()
			elif len(parts) == 3:
				drawn_by = penalty.split("#")[-1][0:2].strip()	
			else:
				print "An unkown error occurred: %s, %s" % (player, penalty)
		else:
			drawn_by = None
		if penalty.find("Fighting \(maj\)") != -1:
			fight = True
		else:
			fight = False
		return {"team" : team, "player" : number, "minutes" : minutes, "drawn_by" : drawn_by, "fight" : fight}
		
	def parseGame(self):
		fp = "reports/" + self.yearID + "/GS/GS" + self.seasonID + self.gameID + ".HTML"
		if not os.path.exists(fp):
			url = "http://www.nhl.com/scores/htmlreports/" + self.yearID + "/GS" + self.seasonID + self.gameID + ".HTM"
			try:
				req = urlopen(url)
				sum_html = req.read()
				f = open(fp, 'w')
				for x in sum_html:
					f.write(x)
				f.close()
					
			except:
				print url
		else:
			f = open(fp, 'r')
			sum_html = f.read()
			f.close()

		sumParse = summaryParser()
		sumParse.feed(sum_html)

		homeTeam = sumParse.home_team_data[2].strip()
		homeTeamShortName = vars.longNameToShortName[homeTeam]
		homeTeamID = vars.longNameToID[homeTeam]
		homeScore = sumParse.home_team_data[1]

		awayTeam = sumParse.away_team_data[2].strip()
		awayTeamShortName = vars.longNameToShortName[awayTeam]
		awayTeamID = vars.longNameToID[awayTeam]
		awayScore = sumParse.away_team_data[1]
		
		if homeScore > awayScore:
			winningGoal = {"team" : homeTeamID, "goal" : int(awayScore) + 1}
		else:
			winningGoal = {"team" : awayTeamID, "goal" : int(homeScore) + 1}

		fp = "reports/" + self.yearID + "/BX/BX" + self.seasonID + self.gameID + ".HTML"
		if not os.path.exists(fp):
			url = "http://www.nhl.com/gamecenter/en/boxscore?id=" + self.yearID[0:4] + self.seasonID + self.gameID
			try:
				req = urlopen(url)
				box_html = req.read()
				f = open(fp, 'w')
				for x in box_html:
					f.write(x)
				f.close()
			except:
				print url
		else:
			f = open(fp, 'r')
			box_html = f.read()
			f.close()

		boxParse = boxParser()
		boxParse.feed(box_html)

		teamInsert = []

		for t in boxParse.away_skaters:
			self.awayTeamSkaters[t[0]] =  self.makeSkater(t[1])
			self.awayTeamSkaters[t[0]]['plusminus'] = t[7]
			self.awayTeamSkaters[t[0]]['timeonice'] = t[-1]

		for t in boxParse.away_goalies:
			shots = t[7].split(" - ")
			saves = shots[0].strip()
			goals_against = str(int(shots[1].strip()) - int(saves))
			self.awayTeamSkaters[t[0]] =  self.makeSkater(t[1])
			self.awayTeamSkaters[t[0]]['saves'] = saves
			self.awayTeamSkaters[t[0]]['goalsagainst'] = goals_against
			
			if len(boxParse.home_goalies) == 1 and t[8] == '1.000' and goals_against == 0:
				self.awayTeamSkaters[t[0]]['shutouts'] = 1

			if t[3].find("(W)") != -1:
				self.awayTeamSkaters[t[0]]['wins'] = 1
			elif boxParse.overtime:
				self.awayTeamSkaters[t[0]]['otlosses'] = 1
			else:
				self.awayTeamSkaters[t[0]]['losses'] = 1
			
			self.awayTeamSkaters[t[0]]['timeonice'] = t[-1]

		for t in boxParse.home_skaters:
			self.homeTeamSkaters[t[0]] =  self.makeSkater(t[1])
			self.homeTeamSkaters[t[0]]['plusminus'] = t[7]
			self.homeTeamSkaters[t[0]]['timeonice'] = t[-1]

		for t in boxParse.home_goalies:
			shots = t[7].split(" - ")
			saves = shots[0].strip()
			goals_against = str(int(shots[1].strip()) - int(saves))
			self.homeTeamSkaters[t[0]] =  self.makeSkater(t[1])
			self.homeTeamSkaters[t[0]]['saves'] = saves
			self.homeTeamSkaters[t[0]]['goalsagainst'] = goals_against
			
			if len(boxParse.home_goalies) == 1 and t[8] == '1.000' and goals_against == 0:
				self.homeTeamSkaters[t[0]]['shutouts'] = 1

			if t[3].find("(W)") != -1:
				self.homeTeamSkaters[t[0]]['wins'] = 1
			elif boxParse.overtime:
				self.homeTeamSkaters[t[0]]['otlosses'] = 1
			else:
				self.homeTeamSkaters[t[0]]['losses'] = 1
			
			self.homeTeamSkaters[t[0]]['timeonice'] = t[-1]
		
		homeGoalCount = 0
		awayGoalCount = 0
		goalModifiers = []
		
		for x in boxParse.goals_data:
			if vars.shortNameToID[x[1]] == homeTeamID:
				homeGoalCount += 1
				if winningGoal['team'] == homeTeamID:
					if homeGoalCount == winningGoal['goal']:
						goalModifiers.append({"team" : vars.idToShortName[winningGoal['team'] ], "goal" : winningGoal['goal'], "modifier" : "GW"})
			else:
				awayGoalCount += 1
				if winningGoal['team'] == awayTeamID:
					if awayGoalCount == winningGoal['goal']:
						goalModifiers.append({"team" : vars.idToShortName[winningGoal['team'] ], "goal" : winningGoal['goal'], "modifier" : "GW"})
						
			if "PS" in x[2]:
				if vars.shortNameToID[x[1]] == homeTeamID:
					goal = homeGoalCount
				else:
					goal = awayGoalCount
				goalModifiers.append({"team" : x[1], "goal" : goal, "modifier" : "PS"})
			if "EN"  in x[2]:
				if vars.shortNameToID[x[1]] == homeTeamID:
					goal = homeGoalCount
				else:
					goal = awayGoalCount
				goalModifiers.append({"team" : x[1], "goal" : goal, "modifier" : "EN"})
		
		starCount = 1
		for x in sumParse.stars_data:
			number = x[3].split(" ")[0]
			hockey_team_name = self.convertHockeyTeamName(x[1])

			if homeTeamID == vars.shortNameToID[hockey_team_name]:
				if starCount == 1:
					self.homeTeamSkaters[number]['firststars'] += 1;
				elif starCount == 2:
					self.homeTeamSkaters[number]['secondstars'] += 1;
				elif starCount == 3:
					self.homeTeamSkaters[number]['thirdstars'] += 1;
				else:
					print "Whoops: %s" % x
			else:
				if starCount == 1:
					self.awayTeamSkaters[number]['firststars'] += 1;
				elif starCount == 2:
					self.awayTeamSkaters[number]['secondstars'] += 1;
				elif starCount == 3:
					self.awayTeamSkaters[number]['thirdstars'] += 1;
				else:
					print "Whoops: %s" % x
			starCount += 1
			
		if "SO" in sumParse.goal_row[-1] and len(sumParse.goal_row[-1]) == 4:
			try:
				fp = "reports/" + self.yearID + "/SO/SO" + self.seasonID + self.gameID.zfill(4) + ".HTML"
				if not os.path.exists(fp):
					url = "http://www.nhl.com/scores/htmlreports/" + self.yearID + "/SO" + self.seasonID + self.gameID + ".HTM"
					print url
					req = urlopen(url)
					shootout_html = req.read()
					f = open(fp, 'w')
					for line in shootout_html:
						f.write(line)
					f.close()
				else:
					f = open(fp, 'r')
					shootout_html = f.read()
					f.close()
					
				shootoutParse = shootoutParser()
				shootoutParse.feed(shootout_html)
			
				for x in shootoutParse.shots:
					if vars.shortNameToID[self.convertHockeyTeamName(x[1])] == homeTeamID:
						if x[5] == 'G':
							if x[3].split(" ")[0]:
								self.homeTeamSkaters[x[3].split(" ")[0].strip()]['shootoutgoals'] += 1
							else:
								print "An unknown error occurred: %s - %s" % (self.seasonID, self.gameID)
							if x[4].split(" ")[0]:	
								self.awayTeamSkaters[x[4].split(" ")[0].strip()]['shootoutgoalsagainst'] += 1
							else:
								if len(boxParse.away_goalies) == 1:
									self.awayTeamSkaters[boxParse.away_goalies[0][0]]['shootoutgoalsagainst'] += 1
								else:
									print "An unknown error occurred: %s - %s"  % (self.seasonID, self.gameID)
						else:
							if x[3].split(" ")[0]:
								self.homeTeamSkaters[x[3].split(" ")[0].strip()]['shootoutmisses'] += 1
							else:
								print "An unknown error occurred: %s - %s" % (self.seasonID, self.gameID)
							if x[4].split(" ")[0]:
								self.awayTeamSkaters[x[4].split(" ")[0].strip()]['shootoutsaves'] += 1
							else:
								if len(boxParse.away_goalies) == 1:
									self.awayTeamSkaters[boxParse.away_goalies[0][0]]['shootoutsaves'] += 1
								else:
									print "An unknown error occurred: %s - %s"  % (self.seasonID, self.gameID)
							
					else:
						if x[5] == 'G':
							if x[3].split(" ")[0]:
								self.awayTeamSkaters[x[3].split(" ")[0].strip()]['shootoutgoals'] += 1
							else:
								print "An unknown error occurred: %s - %s" % (self.seasonID, self.gameID)
							if x[4].split(" ")[0]:
								self.homeTeamSkaters[x[4].split(" ")[0].strip()]['shootoutgoalsagainst'] += 1
							else:
								if len(boxParse.home_goalies) == 1:
									self.awayTeamSkaters[boxParse.away_goalies[0][0]]['shootoutgoalsagainst'] += 1
								else:
									print "An unknown error occurred: %s - %s"  % (self.seasonID, self.gameID)
						else:
							if x[3].split(" ")[0]:
								self.awayTeamSkaters[x[3].split(" ")[0].strip()]['shootoutmisses'] += 1
							else:
								print "An unknown error occurred: %s - %s" % (self.seasonID, self.gameID)
							if x[4].split(" ")[0]:
								self.homeTeamSkaters[x[4].split(" ")[0].strip()]['shootoutsaves'] += 1
							else:
								if len(boxParse.home_goalies) == 1:
									self.awayTeamSkaters[boxParse.away_goalies[0][0]]['shootoutsaves'] += 1
								else:
									print "An unknown error occurred: %s - %s"  % (self.seasonID, self.gameID)
								
			except Exception as e:
				print x	
				print 'hi'
				print sys.exc_info()
				print "\n"
				print traceback.print_tb(sys.exc_info()[2])
				print "\n"
		
		fp = "reports/" + self.yearID + "/PL/PL" + self.seasonID + self.gameID + ".HTML"

		if not os.path.exists(fp):
			url = "http://www.nhl.com/scores/htmlreports/" + self.yearID + "/PL" + self.seasonID + self.gameID + ".HTM"
			try:
				req = urlopen(url)
				play_html = req.read()
				f = open(fp, 'w')
				for line in play_html:
					f.write(line)
				f.close()
			except Exception as e:
				print x	
				print 'hi'
				print sys.exc_info()
				print "\n"
				print traceback.print_tb(sys.exc_info()[2])
				print "\n"
		else:
			f = open(fp, 'r')
			play_html = f.read()
			f.close()

		playParse = playParser()
		playParse.feed(play_html)
		
		homeGoalCount = 0
		awayGoalCount = 0
		try:
			for x in playParse.plays:
				if x['play'][4] not in ['GOFF', 'STOP', 'EGT', 'EGPID', 'PSTR', 'PEND', 'GEND', 'SOC', 'EISTR', 'EIEND']:
					if x['play'][5] == 'SHOT':
						playData = self.processShot(x['play'][6])
						if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
							self.homeTeamSkaters[playData['player']]['shots'] += 1;
						else:
							self.awayTeamSkaters[playData['player']]['shots'] += 1;
						
						if playData['psg']:
							if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
								self.awayTeamSkaters[x['away'][0]]['penaltyshotgoalsagainst'] += 1
							else:
								self.homeTeamSkaters[x['home'][0]]['penaltyshotgoalsagainst'] += 1
							
					elif x['play'][5] == 'BLOCK':
						playData = self.processBlock(x['play'][6])
						if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
							if playData['player']:
								self.homeTeamSkaters[playData['player']]['blocks'] += 1;
							if playData['shooter']:
								self.awayTeamSkaters[playData['shooter']]['blockedshots'] += 1
						else:
							if playData['player']:
								self.awayTeamSkaters[playData['player']]['blocks'] += 1;
							if playData['shooter']:
								self.homeTeamSkaters[playData['shooter']]['blockedshots'] += 1

					elif x['play'][5] == 'GIVE':
						playData = self.processGiveaway(x['play'][6], x['play'][7])
						if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
							self.homeTeamSkaters[playData['player']]['giveaways'] += 1;
						else:
							self.awayTeamSkaters[playData['player']]['giveaways'] += 1;
							
					elif x['play'][5] == 'TAKE':
						playData = self.processTakeaway(x['play'][6], x['play'][7])
						if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
							self.homeTeamSkaters[playData['player']]['takeaways'] += 1;
						else:
							self.awayTeamSkaters[playData['player']]['takeaways'] += 1;
					
					elif x['play'][5] == 'HIT':
						playData = self.processHit(x['play'][6])
						if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
							if playData['player']:
								self.homeTeamSkaters[playData['player']]['hits'] += 1;
							if playData['receiver']:
								self.awayTeamSkaters[playData['receiver']]['hitstaken'] += 1;
						else:
							if playData['player']:
								self.awayTeamSkaters[playData['player']]['hits'] += 1;
							if playData['receiver']:
								self.homeTeamSkaters[playData['receiver']]['hitstaken'] += 1;
							
					elif x['play'][5] == 'FAC':
						playData = self.processFaceOff(x['play'][6])
						if playData['playerOneTeam'] == playData['winnerTeam']:
							if vars.shortNameToID[self.convertHockeyTeamName(playData['winnerTeam'])] == homeTeamID:
								self.homeTeamSkaters[playData['playerOne']]['faceoffwins'] += 1;
								self.awayTeamSkaters[playData['playerTwo']]['faceofflosses'] += 1;
							else:
								self.awayTeamSkaters[playData['playerOne']]['faceoffwins'] += 1;
								self.homeTeamSkaters[playData['playerTwo']]['faceofflosses'] += 1;
						else:
							if vars.shortNameToID[self.convertHockeyTeamName(playData['winnerTeam'])] == homeTeamID:
								self.homeTeamSkaters[playData['playerTwo']]['faceoffwins'] += 1;
								self.awayTeamSkaters[playData['playerOne']]['faceofflosses'] += 1;
							else:
								self.awayTeamSkaters[playData['playerTwo']]['faceoffwins'] += 1;
								self.homeTeamSkaters[playData['playerOne']]['faceofflosses'] += 1;
					
					elif x['play'][5] == 'GOAL':
						if len(x['play']) == 8:
							playData = self.processGoal(x['play'][6] + x['play'][7])
						else:
							playData = self.processGoal(x['play'][6])
							
						if playData['psg']:
							if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
								self.awayTeamSkaters[x['away'][0]]['penaltyshotgoalsagainst'] += 1
							else:
								self.homeTeamSkaters[x['home'][0]]['penaltyshotgoalsagainst'] += 1
						
						if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
							homeGoalCount += 1
							for y in goalModifiers:
								if y['team'] == playData['team'] and y['goal'] == homeGoalCount:
									if y['modifier'] == "EN":
										self.homeTeamSkaters[playData['shooter']]['emptynetgoals'] += 1
										if playData['assistOne'] is not None:
											self.homeTeamSkaters[playData['assistOne']]['emptynetassists'] += 1
										if playData['assistTwo'] is not None:
											self.homeTeamSkaters[playData['assistTwo']]['emptynetassists'] += 1
									if y['modifier'] == "GW":
										self.homeTeamSkaters[playData['shooter']]['gamewinninggoals'] += 1
										if playData['assistOne'] is not None:
											self.homeTeamSkaters[playData['assistOne']]['gamewinningassists'] += 1
										if playData['assistTwo'] is not None:
											self.homeTeamSkaters[playData['assistTwo']]['gamewinningassists'] += 1
						else:
							awayGoalCount += 1
							for y in goalModifiers:
								if y['team'] == playData['team'] and y['goal'] == awayGoalCount:
									if y['modifier'] == "EN":
										self.awayTeamSkaters[playData['shooter']]['emptynetgoals'] += 1
										if playData['assistOne'] is not None:
											self.awayTeamSkaters[playData['assistOne']]['emptynetassists'] += 1
										if playData['assistTwo'] is not None:
											self.awayTeamSkaters[playData['assistTwo']]['emptynetassists'] += 1
									if y['modifier'] == "GW":
										self.awayTeamSkaters[playData['shooter']]['gamewinninggoals'] += 1
										if playData['assistOne'] is not None:
											self.awayTeamSkaters[playData['assistOne']]['gamewinningassists'] += 1
										if playData['assistTwo'] is not None:
											self.awayTeamSkaters[playData['assistTwo']]['gamewinningassists'] += 1
						
						if x['play'][2] == "EV":
							if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
								self.homeTeamSkaters[playData['shooter']]['goals'] += 1
								if playData['psg']:
									self.homeTeamSkaters[playData['shooter']]['penaltyshotgoals'] += 1
								if playData['assistOne'] is not None:
									self.homeTeamSkaters[playData['assistOne']]['assists'] += 1
								if playData['assistTwo'] is not None:
									self.homeTeamSkaters[playData['assistTwo']]['assists'] += 1
							else:
								self.awayTeamSkaters[playData['shooter']]['goals'] += 1
								if playData['psg']:
									self.awayTeamSkaters[playData['shooter']]['penaltyshotgoals'] += 1
								if playData['assistOne'] is not None:
									self.awayTeamSkaters[playData['assistOne']]['assists'] += 1
								if playData['assistTwo'] is not None:
									self.awayTeamSkaters[playData['assistTwo']]['assists'] += 1
						elif x['play'][2] == "PP":
							if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
								self.homeTeamSkaters[playData['shooter']]['goals'] += 1
								self.homeTeamSkaters[playData['shooter']]['powerplaygoals'] += 1
								if playData['psg']:
									self.homeTeamSkaters[playData['shooter']]['penaltyshotgoals'] += 1
								if playData['assistOne'] is not None:
									self.homeTeamSkaters[playData['assistOne']]['assists'] += 1
									self.homeTeamSkaters[playData['assistOne']]['powerplayassists'] += 1
								if playData['assistTwo'] is not None:
									self.homeTeamSkaters[playData['assistTwo']]['assists'] += 1
									self.homeTeamSkaters[playData['assistTwo']]['powerplayassists'] += 1
							else:
								self.awayTeamSkaters[playData['shooter']]['goals'] += 1
								self.awayTeamSkaters[playData['shooter']]['powerplaygoals'] += 1
								if playData['psg']:
									self.awayTeamSkaters[playData['shooter']]['penaltyshotgoals'] += 1
								if playData['assistOne'] is not None:
									self.awayTeamSkaters[playData['assistOne']]['assists'] += 1
									self.awayTeamSkaters[playData['assistOne']]['powerplayassists'] += 1
								if playData['assistTwo'] is not None:
									self.awayTeamSkaters[playData['assistTwo']]['assists'] += 1
									self.awayTeamSkaters[playData['assistTwo']]['powerplayassists'] += 1
						elif x['play'][2] == "SH":
							if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
								self.homeTeamSkaters[playData['shooter']]['goals'] += 1
								self.homeTeamSkaters[playData['shooter']]['shorthandedgoals'] += 1
								if playData['psg']:
									self.homeTeamSkaters[playData['shooter']]['penaltyshotgoals'] += 1
								if playData['assistOne'] is not None:
									self.homeTeamSkaters[playData['assistOne']]['assists'] += 1
									self.homeTeamSkaters[playData['assistOne']]['shorthandedassists'] += 1
								if playData['assistTwo'] is not None:
									self.homeTeamSkaters[playData['assistTwo']]['assists'] += 1
									self.homeTeamSkaters[playData['assistTwo']]['shorthandedassists'] += 1
							else:
								self.awayTeamSkaters[playData['shooter']]['goals'] += 1
								self.awayTeamSkaters[playData['shooter']]['shorthandedgoals'] += 1
								if playData['psg']:
									self.awayTeamSkaters[playData['shooter']]['penaltyshotgoals'] += 1
								if playData['assistOne'] is not None:
									self.awayTeamSkaters[playData['assistOne']]['assists'] += 1
									self.awayTeamSkaters[playData['assistOne']]['shorthandedassists'] += 1
								if playData['assistTwo'] is not None:
									self.awayTeamSkaters[playData['assistTwo']]['assists'] += 1
									self.awayTeamSkaters[playData['assistTwo']]['shorthandedassists'] += 1
						else:
							print "Whoops: %s" % x['play']
						
					elif x['play'][5] == 'MISS':
						playData = self.processMiss(x['play'][6])
						if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
							self.homeTeamSkaters[playData['player']]['misses'] += 1
						else:
							self.awayTeamSkaters[playData['player']]['misses'] += 1
							
						if playData['psg']:
							if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
								self.awayTeamSkaters[x['away'][0]]['penaltyshotgoalsagainst'] += 1
							else:
								self.homeTeamSkaters[x['home'][0]]['penaltyshotgoalsagainst'] += 1
							
					elif x['play'][5] == 'PENL':
						playData = self.processPenalty(x['play'][6], x['play'][7])
						if playData['player'] != "Team":
							if vars.shortNameToID[self.convertHockeyTeamName(playData['team'])] == homeTeamID:
								if playData['player']:
									self.homeTeamSkaters[playData['player']]['pims'] += int(playData['minutes'])
								if playData['drawn_by']:
									self.awayTeamSkaters[playData['drawn_by']]['pimsdrawn'] += int(playData['minutes'])
								if playData['fight']:
									self.homeTeamSkaters[playData['player']]['fights'] += 1
									self.awayTeamSkaters[playData['drawn_by']]['fights'] += 1
							else:
								if playData['player']:
									self.awayTeamSkaters[playData['player']]['pims'] += int(playData['minutes'])
								if playData['drawn_by']:
									self.homeTeamSkaters[playData['drawn_by']]['pimsdrawn'] += int(playData['minutes'])
								if playData['fight']:
									self.awayTeamSkaters[playData['player']]['fights'] += 1
									self.homeTeamSkaters[playData['drawn_by']]['fights'] += 1
		
		except Exception as e:
			print "%s: %s" % (self.gameID, x)	
			print sys.exc_info()
			print "\n"
			print traceback.print_tb(sys.exc_info()[2])
			print "\n"
