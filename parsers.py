#Contains all of the HTML parsers to pull data from NHL.com

from HTMLParser import HTMLParser

class boxParser(HTMLParser):
		def __init__(self):
			HTMLParser.__init__(self)
			
			self.rec = 0
			self.goals_rec = 0
			self.tr_rec = 0
			self.goals_tr_rec = 0
			self.count = 0
			self.scoringcheck = 0
			self.ot_check = 0
			self.prd_span_check = 0
			self.overtime = 0
			self.data = []
			self.goals_data = []
			self.home_skaters = []
			self.home_goalies = []
			self.away_skaters = []
			self.away_goalies = []
			
		def handle_starttag(self, tag, attributes):
			if tag == "div":
				for name,value in attributes:
					if name == "class" and value == "primary":
						self.scoringcheck = 1
				for name,value in attributes:
					if name == "class" and value == "boxData":
						self.prd_span_check = 1
			if tag == "table":
				for name,value in attributes:
					if name == "class" and value == "stats":
						self.rec += 1
					if name == "class" and value == "summary":
						if self.goals_div:
							self.goals_rec += 1
							
			if tag == "span" and self.prd_span_check:
				self.ot_check = 1

			if self.rec > 0 and self.rec <= 4:
				if tag == "tr":
					self.tr_rec = 1
				if self.count > 0:
					for name, value in attributes:
						if name=='href':
							id = value.split('=')
							id = id[1]
							self.data.append(id)
			
			if self.goals_rec > 0:
				if tag == "tr":
					self.goals_tr_rec = 1
			
			
		
		def handle_data(self, data):
			if self.tr_rec == 1:
				self.data.append(data)
				self.count += 1
			if self.goals_tr_rec:
				self.data.append(data.strip())
			if self.scoringcheck:
				if data == "Scoring Summary":
					self.goals_div = 1
			if self.ot_check:
				self.overtime = 1
		
		def handle_endtag(self, tag):
			if self.rec > 0:
				if tag == "tr":
					if self.rec == 1:
						if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
							self.away_skaters.append(self.data)
					elif self.rec == 2:
						if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
							self.away_goalies.append(self.data)
					elif self.rec == 3:
						if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
							self.home_skaters.append(self.data)
					elif self.rec == 4:
						if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
							self.home_goalies.append(self.data)
					self.data = []
					self.count = 0

				if tag == "table" and self.rec == 4:
					self.rec += 1
			
			if tag == "span" and self.ot_check:
				self.prd_span_check = 0
				self.ot_check = 0
					
			if self.goals_rec:
				if tag == "tr":
					if "Period" not in self.data and "\n\n" not in self.data and "\xc2\xa0" not in self.data and 'NONE' not in self.data and 'OT Period' not in self.data:
						self.goals_data.append(self.data)
					self.data = []
					self.goals_tr_rec = 0
				
				if tag == "table":
					self.goals_rec = 0
					self.goals_div = 0
			
			if self.scoringcheck:
				self.scoringcheck = 0
				

class playParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.plays 		= []
		self.home_ice	= []
		self.away_ice	= []
		self.play_data 	= []
		self.t_count 	= 0
		self.rec 		= 0
		self.on_ice_rec	= 0
		self.team		= 0
		self.td_rec		= 0
		self.td_count	= 0

	def handle_starttag(self, tag, attributes):
		if tag == "tr":
			for name, value in attributes:
				if name == "class" and value == "evenColor":
					self.rec = 1

		if tag == "table" and self.rec:
			self.t_count += 1
		
		if tag == "font":
			self.on_ice_rec = 1
			
		if tag == "td" and self.td_rec:
			self.td_count += 1
		
		if tag == "td":
			for name, value in attributes:
				if name == "class":
					if "rborder" in value:
						self.team = 0
						self.td_rec = 1
						self.td_count = 1
			
	def handle_data(self, data):
		if self.rec and self.t_count == 0:
			if data != '\r\n' and data != '\r\r\n':
				self.play_data.append(data)
		
		if self.on_ice_rec:
			if self.team == 0:
				self.away_ice.append(data)
			else:
				self.home_ice.append(data)

	def handle_endtag(self, tag):
		if tag == "table" and self.rec:
			self.t_count -= 1

		if tag == "tr" and self.rec and self.t_count == 0:
			if self.play_data != []:
				if "Elapsed" not in self.play_data and "Description" not in self.play_data:
					tmp_dict = {'play' : self.play_data, 'home' : self.home_ice, 'away' : self.away_ice }
					self.plays.append(tmp_dict)
				self.play_data = []
				self.home_ice = []
				self.away_ice = []
		
		if tag == "font":
			self.on_ice_rec = 0
			
		if tag == "td" and self.td_rec:
			self.td_count -= 1
			
		if self.td_rec and self.td_count == 0:
			self.td_rec = 0
			self.team = 1

class playerParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.table = 0
		self.rec = 0
		self.player_data = []
		self.player = []
		self.count = 0

	def handle_starttag(self, tag, attributes):
		if tag == "table":
			for name, value in attributes:
				if name == "class" and "data stats" in value:
					self.table = 1
					
		if self.table:
			if tag == 'tr':
				self.rec = 1
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
			if '\nPlayer\n' not in self.player_data and ' | ' not in self.player_data:
				self.player.append(self.player_data)
			self.rec = 0
			self.player_data = []
			self.count = 0
		if tag == 'tbody':
			self.table = 0
			
class summaryParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		
		self.home_team_data = []
		self.home_rec = 0
		
		self.away_team_data = []
		self.away_rec = 0

		self.summary_rec = 0
		self.summary_data = []
		self.append = 0

		self.goal_rec = 0
		self.goal_row = []
		self.goal_row_rec = 0
		self.goal_row_data = []

		self.stars_rec = 0
		self.stars_row = []
		self.stars_data = []

	def handle_starttag(self, tag, attributes):
		if tag == "table":
			for name,value in attributes:
				if name == "id" and value == "Visitor":
					self.away_rec = 1
			
				if name =="id" and value == "GameInfo":
					self.away_rec = 0
					self.summary_rec = 1

				if name == "id" and value == "Home":
					self.home_rec = 1
					self.summary_rec = 0
		
		if tag == "tr" and self.goal_rec:
			self.goal_row_rec = 1

	def handle_data(self, data):
		if self.home_rec:
			if data != "" and data != "\r\n" and data != "\r\r\n" and "Match/Game" not in data and "SCORING SUMMARY" not in data:
				self.home_team_data.append(data)
		if self.away_rec:
			if data != "" and data != "\r\n" and data != "\r\r\n" and "Match/Game" not in data and "SCORING SUMMARY" not in data:
				self.away_team_data.append(data)
		if self.summary_rec:
			if data != "\r\n" and data != "\r\r\n" and data != ", " and data != "Sommaire du Match":
				if self.append:
					end_row = self.summary_data.pop()
					end_row += data
					self.summary_data.append(end_row)
					self.append = 0
				else:
					self.summary_data.append(data)
		
		if "SCORING SUMMARY" in data:
			self.goal_rec = 1
			
		if "PENALTY SUMMARY" in data:
			self.goal_rec = 0

		if self.stars_rec:
			if data != "\r\n" and data != "\r\r\n":
				self.stars_row.append(data)

		if "3 STARS" in data:
			self.stars_rec = 1
		
		if self.goal_row_rec:
			if data != "\r\n" and data != "\r\r\n" and data != ", ":
				self.goal_row_data.append(data)
	
	def handle_endtag(self, tag):
		if self.stars_rec:
			if tag == "tr":
				if self.stars_row != [] and len(self.stars_row) == 4:
					self.stars_data.append(self.stars_row)
				self.stars_row = []
		if self.goal_row_rec and tag == "tr":
			self.goal_row_rec = 0
			if "Time" not in self.goal_row_data and len(self.goal_row_data) > 3:
				self.goal_row.append(self.goal_row_data)
			self.goal_row_data = []
				
	def handle_entityref(self, name):
		if name == "amp":
			self.append = 1
			
class shootoutParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.rec = 0
		self.shot_data = []
		self.shots = []

	def handle_starttag(self, tag, attributes):
		if tag == "tr":
			for name, value in attributes:
				if name == "class" and (value == "oddColor + " or value == "evenColor + " or value == "oddColor + bold" or value == "evenColor + bold"):
					self.rec = 1

	def handle_data(self, data):
		if self.rec:
			if data != "\r\n":
				self.shot_data.append(data)

	def handle_endtag(self, tag):
		if tag == 'tr' and self.rec:
			self.shots.append(self.shot_data)
			self.rec = 0
			self.shot_data = []

class seasonParser(HTMLParser):
        def __init__(self):
                HTMLParser.__init__(self)
                self.recording = 0
                self.games = []
                self.data = []

        def handle_starttag(self, tag, attributes):
                if tag == 'table':
                        for name, value in attributes:
                                if name == 'class' and value == 'data schedTbl':
                                        self.recording = 1

        def handle_endtag(self, tag):
                if tag == 'tr' and self.recording:
                        if "VISITING TEAM" not in self.data:
                                self.games.append(self.data)
                        self.data = []

        def handle_data(self, data):
                if self.recording:
                        self.data.append(data)

