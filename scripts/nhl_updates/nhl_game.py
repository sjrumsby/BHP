from urllib2 import urlopen
from parsers import *
import json
import os
import re
import sys
import vars
import logging

logger = logging.getLogger(__name__)

class nhl_game(): 
    def __init__(self, season, game, year, update_html = False):
        self.seasonID = season
        self.gameID = game
        self.yearID = year
        self.homeTeamSkaters = {}
        self.awayTeamSkaters = {}
        self.update_html = update_html
        self.homeScore = 0
        self.awayScore = 0
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
                self.pretty(value, indent+1)
            else:
                print '\t\t' * (indent+1) + str(value)

    def print_to_file(self, homeTeamSkaters, awayTeamSkaters):
        fp = "JSON/" + self.yearID + "/" + self.gameID + "_home.json"
        f = open(fp, 'w')
        f.write('{ \n')
        for key, value in homeTeamSkaters.iteritems():
            f.write('\t"' + str(key) + '" : ' + '{\n')
            if isinstance(value, dict):
                for key2, value2 in homeTeamSkaters[key].iteritems():
                    f.write( '\t\t"' + str(key2) + '" : "' + str(value2) + '",\n')
                f.write( '\t\n},')
        f.write( '}\n')
        
        fp = "JSON/" + self.yearID + "/" + self.gameID + "_away.json"
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
        if play['team']['id'] == self.homeTeamID:
            winnerTeam = self.homeTeamID
        else:
            winnerTeam = self.awayTeamID

        for p in play['players']:
            if p['playerType'] == 'Winner':
                winner = p['player']['id']
            else:
                loser = p['player']['id']
        return {"winner" : winner, "loser" : loser, "winnerTeam" : winnerTeam}

    def processBlock(self, play):
        if play['team']['id'] == self.homeTeamID:
            team = self.homeTeamID
            shooterTeam = self.awayTeamID
        else:
            team = self.awayTeamID
            shooterTeam = self.homeTeamID

        for p in play['players']:
            if p['playerType'] == 'Blocker':
                blocker = p['player']['id']
            else:
                shooter = p['player']['id']

        return {"player" : blocker, "team" : team, "shooter" : shooter, "shooter_team" : shooterTeam}

    def processShot(self, play):
        if play['team']['id'] == self.homeTeamID:
            team = self.homeTeamID
        else:
            team = self.awayTeamID

        for p in play['players']:
            if p['playerType'] == 'Shooter':
                shooter = p['player']['id']

        if "Penalty Shot" in play:
            psg = True
        else:
            psg = False

        return {"shooter" : shooter, "team" : team, "psg" : psg}
        
    def processGiveaway(self, play):
        if play['team']['id'] == self.homeTeamID:
            team = self.homeTeamID
        else:
            team = self.awayTeamID

        return {"player" : play['players'][0]['player']['id'], "team" : team}

    def processTakeaway(self, play):
        if play['team']['id'] == self.homeTeamID:
            team = self.homeTeamID
        else:
            team = self.awayTeamID

        return {"player" : play['players'][0]['player']['id'], "team" : team}

    def processMiss(self, play):
        if play['team']['id'] == self.homeTeamID:
            team = self.homeTeamID
        else:
            team = self.awayTeamID

        if "Penalty Shot" in play:
            psg = True
        else:
            psg = False
        return {"player" : play['players'][0]['player']['id'], "team" : team, "psg" : psg}

    def processHit(self, play):
        if play['team']['id'] == self.homeTeamID:
            hitterTeam = self.homeTeamID
        else:
            hitterTeam = self.awayTeamID

        for p in play['players']:
            if p['playerType'] == 'Hitter':
                hitter = p['player']['id']
            else:
                hittee = p['player']['id']
        return {"hitterTeam" : hitterTeam, "hitter" : hitter, "hittee" : hittee}

    def processGoal(self, play):
        if play['team']['id'] == self.homeTeamID:
            team = self.homeTeamID
        else:
            team = self.awayTeamID

        scorer = None
        assistOne = None
        assistTwo = None

        for p in play['players']:
            if p['playerType'] == 'Scorer':
                scorer = p['player']['id']
            if p['playerType'] == 'Assist':
                if assistOne == None:
                    assistOne = p['player']['id']
                else:
                    assistTwo = p['player']['id']
        if "Penalty Shot" in play:
            psg = True
        else:
            psg = False

        return {"team" : team, "scorer"  : scorer, "assistOne" : assistOne, "assistTwo" : assistTwo, "psg" : psg, "strength" : play['result']['strength']['code']}

    def processPenalty(self, play):
        if play['team']['id'] == self.homeTeamID:
            team = self.homeTeamID
        else:
            team = self.awayTeamID

        player = None
        drawn_by = None

        for p in play['players']:
            if p['playerType'] == 'PenaltyOn':
                player = p['player']['id']
            if p['playerType'] == 'DrewBy':
                if team == self.homeTeamID:
#If a player serves a penalty for their own teammate, they go down as the "DrewBy" as well
                    if p['player']['id'] not in self.homeTeamSkaters:
                        drawn_by = p['player']['id']
                else:
                    if p['player']['id'] not in self.awayTeamSkaters:
                        drawn_by = p['player']['id']

        if play['result']['description'].find("Fighting (maj)") != -1:
            fight = True
        else:
            fight = False
        return {"team" : team, "player" : player, "minutes" : play['result']['penaltyMinutes'], "drawn_by" : drawn_by, "fight" : fight}
        
    def parseGame(self):
        boxJsonURL = 'http://statsapi.web.nhl.com/api/v1/game/%s/feed/live?site=en_nhl' % (self.yearID[0:4] + self.seasonID + self.gameID)
        try:
            req = urlopen(boxJsonURL)
            boxJSON = req.read()
            boxData = json.loads(boxJSON)
        except Exception:
            import traceback
            print "Exception %s" % traceback.format_exc()

        homeTeam = boxData['gameData']['teams']['home']['name']
        homeTeamShortName = boxData['gameData']['teams']['home']['abbreviation']
        self.homeTeamID =  boxData['gameData']['teams']['home']['id']
        self.homeScore = boxData['liveData']['linescore']['teams']['home']['goals']
        
        awayTeam = boxData['gameData']['teams']['away']['name']
        awayTeamShortName = boxData['gameData']['teams']['away']['abbreviation']
        self.awayTeamID =  boxData['gameData']['teams']['away']['id']
        self.awayScore = boxData['liveData']['linescore']['teams']['away']['goals']

        for t in boxData['liveData']['boxscore']['teams']['away']['players']:
            currentPlayer = boxData['liveData']['boxscore']['teams']['away']['players'][t]
            self.awayTeamSkaters[currentPlayer['person']['id']] = self.makeSkater(currentPlayer['person']['id'])
            if currentPlayer['position']['code'] == 'G':
                self.awayTeamSkaters[currentPlayer['person']['id']]['saves'] = currentPlayer['stats']['goalieStats']['saves']
                self.awayTeamSkaters[currentPlayer['person']['id']]['goalsagainst'] = currentPlayer['stats']['goalieStats']['shots'] - currentPlayer['stats']['goalieStats']['saves']

                if 'decision' in currentPlayer['stats']['goalieStats']:
                    if self.awayTeamSkaters[currentPlayer['person']['id']]['goalsagainst'] == 0:
                        self.awayTeamSkaters[currentPlayer['person']['id']]['shutouts'] = 1
                    else:
                        self.awayTeamSkaters[currentPlayer['person']['id']]['shutouts'] = 0
                
                    if currentPlayer['stats']['goalieStats']['decision'] == 'W':
                        self.awayTeamSkaters[currentPlayer['person']['id']]['wins'] = 1
                    else:
                        self.awayTeamSkaters[currentPlayer['person']['id']]['wins'] = 0
                
                    if currentPlayer['stats']['goalieStats']['decision'] == 'OTL':
                        self.awayTeamSkaters[currentPlayer['person']['id']]['otlosses'] = 1
                    else:
                        self.awayTeamSkaters[currentPlayer['person']['id']]['otlosses'] = 0
            
            else:
                if currentPlayer['stats'] != {}:
                    self.awayTeamSkaters[currentPlayer['person']['id']]['plusminus'] = currentPlayer['stats']['skaterStats']['plusMinus']
                    self.awayTeamSkaters[currentPlayer['person']['id']]['timeonice'] = currentPlayer['stats']['skaterStats']['timeOnIce']

        for t in boxData['liveData']['boxscore']['teams']['home']['players']:
            currentPlayer = boxData['liveData']['boxscore']['teams']['home']['players'][t]
            self.homeTeamSkaters[currentPlayer['person']['id']] = self.makeSkater(currentPlayer['person']['id'])
            if currentPlayer['position']['code'] == 'G':
                self.homeTeamSkaters[currentPlayer['person']['id']]['saves'] = currentPlayer['stats']['goalieStats']['saves']
                self.homeTeamSkaters[currentPlayer['person']['id']]['goalsagainst'] = currentPlayer['stats']['goalieStats']['shots'] - currentPlayer['stats']['goalieStats']['saves']

                if 'decision' in currentPlayer['stats']['goalieStats']:
                    if self.homeTeamSkaters[currentPlayer['person']['id']]['goalsagainst'] == 0:
                        self.homeTeamSkaters[currentPlayer['person']['id']]['shutouts'] = 1
                    else:
                        self.homeTeamSkaters[currentPlayer['person']['id']]['shutouts'] = 0
                
                    if currentPlayer['stats']['goalieStats']['decision'] == 'W':
                        self.homeTeamSkaters[currentPlayer['person']['id']]['wins'] = 1
                    else:
                        self.homeTeamSkaters[currentPlayer['person']['id']]['wins'] = 0
                
                    if currentPlayer['stats']['goalieStats']['decision'] == 'OTL':
                        self.homeTeamSkaters[currentPlayer['person']['id']]['otlosses'] = 1
                    else:
                        self.homeTeamSkaters[currentPlayer['person']['id']]['otlosses'] = 0

            else:
                if currentPlayer['stats'] != {}:
                    self.homeTeamSkaters[currentPlayer['person']['id']]['plusminus'] = currentPlayer['stats']['skaterStats']['plusMinus']
                    self.homeTeamSkaters[currentPlayer['person']['id']]['timeonice'] = currentPlayer['stats']['skaterStats']['timeOnIce']

        try:
            firstStar = boxData['liveData']['decisions']['firstStar']['id']
            if firstStar in self.homeTeamSkaters:
                    self.homeTeamSkaters[firstStar]['firststars'] += 1
            else:
                self.awayTeamSkaters[firstStar]['firststars'] += 1
        except:
            logger.info('No first stars exists in game: %s' % self.yearID[0:4] + self.seasonID + self.gameID)
        try:
            secondStar = boxData['liveData']['decisions']['secondStar']['id']
            if secondStar in self.homeTeamSkaters:
                self.homeTeamSkaters[secondStar]['secondstars'] += 1
            else:
                self.awayTeamSkaters[secondStar]['secondstars'] += 1
        except:
            logger.info('No second stars exists in game: %s' % self.yearID[0:4] + self.seasonID + self.gameID)

        try:
            thirdStar = boxData['liveData']['decisions']['thirdStar']['id']
            if thirdStar in self.homeTeamSkaters:
                self.homeTeamSkaters[thirdStar]['thirdstars'] += 1
            else:
                self.awayTeamSkaters[thirdStar]['thirdstars'] += 1
        except:
            logger.info('No third stars exists in game: %s' % self.yearID[0:4] + self.seasonID + self.gameID)

        homeGoalCount = 0
        awayGoalCount = 0
        goalModifiers = []

        if not boxData['liveData']['linescore']['hasShootout']:
            try:
                winningGoalPlay = boxData['liveData']['plays']['allPlays'][boxData['liveData']['plays']['scoringPlays'][-1]]
                for player in winningGoalPlay['players']:
                    try:
                        if player['playerType'] == 'Scorer':
                            self.homeTeamSkaters[player['player']['id']]['gamewinninggoals'] += 1
                        else:
                            self.homeTeamSkaters[player['player']['id']]['gamewinningassists'] += 1
                    except:
                        if player['playerType'] == 'Scorer':
                            self.awayTeamSkaters[player['player']['id']]['gamewinninggoals'] += 1
                        else:
                            self.awayTeamSkaters[player['player']['id']]['gamewinningassists'] += 1
            except:
                pass
        else:
            try:
                    winnerGoalie = boxData['liveData']['decisions']['winner']['id']
            except:
                winnerGoalie = ''
            try:
                    loserGoalie = boxData['liveData']['decisions']['loser']['id']
            except:
                loserGoalie = ''
            for x in boxData['liveData']['plays']['allPlays'][boxData['liveData']['plays']['playsByPeriod'][-1]['startIndex']::]:
                if x['result']['eventTypeId'] not in ['PERIOD_READY', 'PERIOD_START', 'SHOOTOUT_COMPLETE', 'PERIOD_END', 'PERIOD_OFFICIAL', 'GAME_END']:
                    if x['result']['eventTypeId'] == 'GOAL':
                        for p in x['players']:
                            if p['playerType'] == 'Shooter':
                                if p['player']['id'] in self.homeTeamSkaters:
                                    self.homeTeamSkaters[p['player']['id']]['shootoutgoals'] += 1
                                    if winnerGoalie in self.awayTeamSkaters:
                                        self.awayTeamSkaters[winnerGoalie]['shootoutgoalsagainst'] += 1
                                    elif winnerGoalie in self.awayTeamSkaters:
                                        self.awayTeamSkaters[loserGoalie]['shootoutgoalsagainst'] += 1
                                else:
                                    self.awayTeamSkaters[p['player']['id']]['shootoutgoals'] += 1
                                    if winnerGoalie in self.homeTeamSkaters:
                                        self.homeTeamSkaters[winnerGoalie]['shootoutgoalsagainst'] += 1
                                    elif winnerGoalie in self.awayTeamSkaters:
                                        self.homeTeamSkaters[loserGoalie]['shootoutgoalsagainst'] += 1
                    else:
                        for p in x['players']:
                            if p['playerType'] == 'Shooter':
                                if p['player']['id'] in self.homeTeamSkaters:
                                    self.homeTeamSkaters[p['player']['id']]['shootoutmisses'] += 1
                                    if winnerGoalie in self.awayTeamSkaters:
                                        self.awayTeamSkaters[winnerGoalie]['shootoutsaves'] += 1
                                    elif winnerGoalie in self.awayTeamSkaters:
                                        self.awayTeamSkaters[loserGoalie]['shootoutsaves'] += 1
                                else:
                                    self.awayTeamSkaters[p['player']['id']]['shootoutmisses'] += 1
                                    if winnerGoalie in self.homeTeamSkaters:
                                        self.homeTeamSkaters[winnerGoalie]['shootoutsaves'] += 1
                                    elif winnerGoalie in self.awayTeamSkaters:
                                        self.homeTeamSkaters[loserGoalie]['shootoutsaves'] += 1
        try:
            for x in boxData['liveData']['plays']['allPlays']:
                if x['result']['eventTypeId'] not in ['GOFF', 'STOP', 'EGT', 'EGPID', 'PSTR', 'PEND', 'GEND', 'SOC', 'EISTR', 'EIEND'] and x['about']['periodType'] != 'SHOOTOUT':
                    if x['result']['eventTypeId'] == 'SHOT':
                        playData = self.processShot(x)
                        if playData['team'] == self.homeTeamID:
                            self.homeTeamSkaters[playData['shooter']]['shots'] += 1;
                        else:
                            self.awayTeamSkaters[playData['shooter']]['shots'] += 1;
                        
                        if playData['psg']:
                            logger.error("Need to do something about Penalty shots here")
                            
                    elif x['result']['eventTypeId'] == 'BLOCKED_SHOT':
                        playData = self.processBlock(x)
                        if playData['team'] == self.homeTeamID:
                            if playData['player']:
                                self.homeTeamSkaters[playData['player']]['blocks'] += 1;
                            if playData['shooter']:
                                self.awayTeamSkaters[playData['shooter']]['blockedshots'] += 1
                        else:
                            if playData['player']:
                                self.awayTeamSkaters[playData['player']]['blocks'] += 1;
                            if playData['shooter']:
                                self.homeTeamSkaters[playData['shooter']]['blockedshots'] += 1

                    elif x['result']['eventTypeId'] == 'GIVEAWAY':
                        playData = self.processGiveaway(x)
                        if playData['team'] == self.homeTeamID:
                            self.homeTeamSkaters[playData['player']]['giveaways'] += 1;
                        else:
                            self.awayTeamSkaters[playData['player']]['giveaways'] += 1;
                            
                    elif x['result']['eventTypeId'] == 'TAKEAWAY':
                        playData = self.processTakeaway(x)
                        if playData['team'] == self.homeTeamID:
                            self.homeTeamSkaters[playData['player']]['takeaways'] += 1;
                        else:
                            self.awayTeamSkaters[playData['player']]['takeaways'] += 1;
                    
                    elif x['result']['eventTypeId'] == 'HIT':
                        playData = self.processHit(x)
                        if playData['hitterTeam'] == self.homeTeamID:
                            if playData['hitter']:
                                self.homeTeamSkaters[playData['hitter']]['hits'] += 1
                            if playData['hittee']:
                                self.awayTeamSkaters[playData['hittee']]['hitstaken'] += 1
                        else:
                            if playData['hitter']:
                                self.awayTeamSkaters[playData['hitter']]['hits'] += 1
                            if playData['hittee']:
                                self.homeTeamSkaters[playData['hittee']]['hitstaken'] += 1
                            
                    elif x['result']['eventTypeId'] == 'FACEOFF':
                        playData = self.processFaceOff(x)
                        if playData['winnerTeam'] == self.homeTeamID:
                            self.homeTeamSkaters[playData['winner']]['faceoffwins'] += 1
                            self.awayTeamSkaters[playData['loser']]['faceofflosses'] += 1
                        else:
                            self.awayTeamSkaters[playData['winner']]['faceoffwins'] += 1
                            self.homeTeamSkaters[playData['loser']]['faceofflosses'] += 1
                    
                    elif x['result']['eventTypeId'] == 'GOAL':
                        playData = self.processGoal(x)

                        if playData['team'] == self.homeTeamID:
                            self.homeTeamSkaters[playData['scorer']]['shots'] += 1
                        else:
                            self.awayTeamSkaters[playData['scorer']]['shots'] += 1

                        if playData['psg']:
                            if playData['team'] == self.homeTeamID:
                                self.awayTeamSkaters[x['away'][0]]['penaltyshotgoalsagainst'] += 1
                            else:
                                self.homeTeamSkaters[x['home'][0]]['penaltyshotgoalsagainst'] += 1
                    
                        if playData['team'] == self.homeTeamID:
                            self.homeTeamSkaters[playData['scorer']]['goals'] += 1
                            if playData['assistOne'] is not None:
                                self.homeTeamSkaters[playData['assistOne']]['assists'] += 1
                            if playData['assistTwo'] is not None:
                                    self.homeTeamSkaters[playData['assistTwo']]['assists'] += 1
                            if playData['strength'] == 'PPG':
                                self.homeTeamSkaters[playData['scorer']]['powerplaygoals'] += 1
                                if playData['assistOne'] is not None:
                                    self.homeTeamSkaters[playData['assistOne']]['powerplayassists'] += 1
                                if playData['assistTwo'] is not None:
                                    self.homeTeamSkaters[playData['assistTwo']]['powerplayassists'] += 1
                            elif playData['strength'] == 'SHG':
                                self.homeTeamSkaters[playData['scorer']]['shorthandedgoals'] += 1
                                if playData['assistOne'] is not None:
                                    self.homeTeamSkaters[playData['assistOne']]['shorthandedassists'] += 1
                                if playData['assistTwo'] is not None:
                                    self.homeTeamSkaters[playData['assistTwo']]['shorthandedassists'] += 1
                        else:
                            self.awayTeamSkaters[playData['scorer']]['goals'] += 1
                            if playData['assistOne'] is not None:
                                self.awayTeamSkaters[playData['assistOne']]['assists'] += 1
                            if playData['assistTwo'] is not None:
                                self.awayTeamSkaters[playData['assistTwo']]['assists'] += 1
                            if playData['strength'] == 'PPG':
                                self.awayTeamSkaters[playData['scorer']]['powerplaygoals'] += 1
                                if playData['assistOne'] is not None:
                                    self.awayTeamSkaters[playData['assistOne']]['powerplayassists'] += 1
                                if playData['assistTwo'] is not None:
                                    self.awayTeamSkaters[playData['assistTwo']]['powerplayassists'] += 1
                            elif playData['strength'] == 'SHG':
                                self.awayTeamSkaters[playData['scorer']]['shorthandedgoals'] += 1
                                if playData['assistOne'] is not None:
                                    self.awayTeamSkaters[playData['assistOne']]['shorthandedassists'] += 1
                                if playData['assistTwo'] is not None:
                                    self.awayTeamSkaters[playData['assistTwo']]['shorthandedassists'] += 1
                    elif x['result']['eventTypeId'] == 'MISSED_SHOT':
                        playData = self.processMiss(x)
                        if playData['team'] == self.homeTeamID:
                            self.homeTeamSkaters[playData['player']]['misses'] += 1
                        else:
                            self.awayTeamSkaters[playData['player']]['misses'] += 1
                            
                        if playData['psg']:
                            if playData['team'] == self.homeTeamID:
                                self.awayTeamSkaters[x['away'][0]]['penaltyshotgoalsagainst'] += 1
                            else:
                                self.homeTeamSkaters[x['home'][0]]['penaltyshotgoalsagainst'] += 1
                            
                    elif x['result']['eventTypeId'] == 'PENALTY':
                        playData = self.processPenalty(x)
                        if playData['player'] != "Team":
                            if playData['team'] == self.homeTeamID:
                                if playData['player']:
                                    self.homeTeamSkaters[playData['player']]['pims'] += int(playData['minutes'])
                                if playData['drawn_by']:
                                    self.awayTeamSkaters[playData['drawn_by']]['pimsdrawn'] += int(playData['minutes'])
                                if playData['fight']:
                                    self.homeTeamSkaters[playData['player']]['fights'] += 1
                            else:
                                if playData['player']:
                                    self.awayTeamSkaters[playData['player']]['pims'] += int(playData['minutes'])
                                if playData['drawn_by']:
                                    self.homeTeamSkaters[playData['drawn_by']]['pimsdrawn'] += int(playData['minutes'])
                                if playData['fight']:
                                    self.awayTeamSkaters[playData['player']]['fights'] += 1


        except Exception as e:
                    import traceback
                    print "%s: %s" % (self.gameID, x)   
                    print sys.exc_info()
                    print "\n"
                    print traceback.print_tb(sys.exc_info()[2])
                    print "\n"
