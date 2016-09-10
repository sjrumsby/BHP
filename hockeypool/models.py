from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime

import logging
logger = logging.getLogger(__name__)

def get_theme(self):
	p = Player.objects.get(id=self.id)
	return p.theme

User.add_to_class("get_theme", get_theme)

class Hockey_Team(models.Model):
        name            = models.CharField(max_length=3)
        full_name       = models.CharField(max_length=24)

        def __unicode__(self):
                return self.name

class Year(models.Model):
	description	= models.CharField(max_length=16)

class Week(models.Model):
        number          = models.IntegerField()
	year		= models.ForeignKey(Year)

        def __unicode__(self):
                return "Week: %s" % self.number

class Pool(models.Model):
        name = models.CharField(max_length=64, default="")
        current_week = models.ForeignKey(Week)
	current_year = models.ForeignKey(Year)

class Game(models.Model):
        date            = models.DateField()
        home_team       = models.ForeignKey(Hockey_Team, related_name="home_team")
        away_team       = models.ForeignKey(Hockey_Team, related_name="away_team")
        time            = models.TimeField()
        nhl_game_id     = models.IntegerField()
	year		= models.ForeignKey(Year)

class Position(models.Model):
	code		= models.CharField(max_length=1)
	long_name	= models.CharField(max_length=16)

class Category_Point(models.Model):
	pool		= models.ForeignKey(Pool)
	name		= models.CharField(max_length=16)
	value		= models.IntegerField()

class Skater(models.Model):
        nhl_id          = models.IntegerField(primary_key=True)
        first_name      = models.CharField(max_length=64, default="")
	last_name       = models.CharField(max_length=64, default="")
	full_name	= models.CharField(max_length=64, default="")
        hockey_team     = models.ForeignKey(Hockey_Team, default=0)
        goals           = models.IntegerField(default=0)
        assists         = models.IntegerField(default=0)
        points          = models.IntegerField(default=0)
        plus_minus      = models.IntegerField(default=0)
        shg             = models.IntegerField(default=0)
        sha             = models.IntegerField(default=0)
        ppg             = models.IntegerField(default=0)
        ppa             = models.IntegerField(default=0)
        gwg             = models.IntegerField(default=0)
	gwa		= models.IntegerField(default=0)
        psg             = models.IntegerField(default=0)
	eng		= models.IntegerField(default=0)
	ena		= models.IntegerField(default=0)
        pims            = models.IntegerField(default=0)
	pims_drawn	= models.IntegerField(default=0)
        hits            = models.IntegerField(default=0)
        shots           = models.IntegerField(default=0)
	blocked_shots	= models.IntegerField(default=0)
        blocks          = models.IntegerField(default=0)
        fights          = models.IntegerField(default=0)
        giveaways       = models.IntegerField(default=0)
        takeaways       = models.IntegerField(default=0)
        faceoff_win     = models.IntegerField(default=0)
        faceoff_loss    = models.IntegerField(default=0)
        shootout_made   = models.IntegerField(default=0)
        shootout_fail   = models.IntegerField(default=0)
        wins            = models.IntegerField(default=0)
        otloss          = models.IntegerField(default=0)
        shutouts        = models.IntegerField(default=0)
        penshot_save    = models.IntegerField(default=0)
        penshot_ga      = models.IntegerField(default=0)
        shootout_save   = models.IntegerField(default=0)
        shootout_ga     = models.IntegerField(default=0)
        saves           = models.IntegerField(default=0)
        goals_against   = models.IntegerField(default=0)
	time_on_ice	= models.CharField(max_length=16, default="0:00")
	first_stars	= models.IntegerField(default=0)
	second_stars	= models.IntegerField(default=0)
	third_stars	= models.IntegerField(default=0)
        fantasy_points  = models.IntegerField(default=0)

	def __init__(self, *args, **kwargs):
		super(Skater, self).__init__(*args, **kwargs)
		current_date = datetime.datetime.now()
		if current_date.month < 10:
			start_date = "%s-%s-%s" % (current_date.year - 1, 10, 1)
			end_date = "%s-%s-%s" % (current_date.year, 4, 30)
		else:
			start_date = "%s-%s-%s" % (current_date.year, 10, 1)
                        end_date = "%s-%s-%s" % (current_date.year + 1, 4, 30)
		self.games_played = Point.objects.filter(skater_id=self.pk).filter(date__range=(start_date, end_date)).count()

	def __unicode__(self):
		return '<span id="skater-%s" nhl_id="%s" class="skaterPopUp"><a href="#">%s</a></span>' % (self.nhl_id, self.nhl_id, self.first_name + " " + self.last_name)

	def get_draft_name(self):
		return '<a href="/skater/%s">%s (%s)</a>' % (self.nhl_id, self.first_name + " " + self.last_name, self.get_position())

	def get_name(self):
		return "%s %s" % (self.first_name, self.last_name)

	def get_owner(self):
		t = Team.objects.filter(skater_id=self.nhl_id)

		if len(t) == 1:
			return t[0].player.name
		else:
			return "Free Agent"

	def get_position(self):
		positions = []

		for x in Skater_Position.objects.filter(skater_id=self.nhl_id).order_by('-position_id'):
			positions.append(x.position.code)

		return ', '.join(positions)

	def get_skater_category_data(self):
		date = datetime.datetime.now()

#Jan 1 + 305 days = ~ October 3. Good enough.

		date = date - datetime.timedelta(days=305)
		season = "%s%s" % (date.year, date.year + 1)
		year = Year.objects.get(description=season)
		p = Point.objects.filter(game__year=year, skater_id=self.nhl_id).values('skater_id').annotate(fantasy_points=Sum('fantasy_points'), goals=Sum('goals'), assists=Sum('assists'), shootout=Sum('shootout'), plus_minus=Sum('plus_minus'), offensive_special=Sum('offensive_special'), true_grit=Sum('true_grit_special'), goalie=Sum('goalie'))

		if len(p) == 1:
			return {'categories': {
					'fantasy_points': p[0]['fantasy_points'], 
					'goals': p[0]['goals'], 
					'assists': p[0]['assists'],
					'plus_minus': p[0]['plus_minus'],
					'specialty': p[0]['offensive_special'],
					'true_grit': p[0]['true_grit'],
					'goalie': p[0]['goalie'],
					'shootout': p[0]['shootout']
				},
				'error': 0
			}
		else:
                        return {'categories': {
                                        'fantasy_points': 0,
                                        'goals': 0,
                                        'assists': 0,
                                        'plus_minus': 0, 
                                        'specialty': 0,
                                        'true_grit': 0,
                                        'goalie': 0,
                                        'shootout': 0 
                                },
                                'error': -1
                        }

class Skater_Position(models.Model):
	skater = models.ForeignKey(Skater)
	position = models.ForeignKey(Position)

class Player(models.Model):
        name            = models.CharField(max_length=32)
        conference      = models.CharField(max_length=4,default="")
	theme		= models.CharField(max_length=64,default="sandstone")
	pool		= models.ForeignKey(Pool)

        def __unicode__(self):
                return '<span class="playerPopUp" id="player-%s" player_id="%s"><a href="#">%s</a></span>' % (self.id, self.id, self.name)

	def get_player_popup_data(self):
		return {}

class Team(models.Model):
        skater          = models.ForeignKey(Skater)
        player          = models.ForeignKey(Player)

class Point(models.Model):
        skater                  = models.ForeignKey(Skater)
        game                    = models.ForeignKey(Game)
        fantasy_points          = models.IntegerField()
        goals                   = models.IntegerField()
        assists                 = models.IntegerField()
        shootout                = models.IntegerField()
        plus_minus              = models.IntegerField()
        offensive_special       = models.IntegerField()
        true_grit_special       = models.IntegerField()
        goalie                  = models.IntegerField()
        date                    = models.DateField()

class Team_Point(models.Model):
        point           = models.ForeignKey(Point)
        player          = models.ForeignKey(Player)
	pool		= models.ForeignKey(Pool)

class Injury(models.Model):
        skater          = models.ForeignKey(Skater)
        date            = models.DateField()
        status          = models.CharField(max_length=128)
        description     = models.CharField(max_length=512)

class Post(models.Model):
        title           = models.CharField(max_length=256)
        text            = models.CharField(max_length=128000)

class Week_Date(models.Model):
        week            = models.ForeignKey(Week)
        date            = models.DateField()


