from django.db import models
from hockeypool.models import *

class Match(models.Model):
        week            = models.ForeignKey(Week)
        home_player     = models.ForeignKey(Player, related_name="home_player", null=True, blank=True, default = None)
        away_player     = models.ForeignKey(Player, related_name="away_player", null=True, blank=True, default = None)
        winner_player   = models.ForeignKey(Player, related_name="winner_player", null=True, blank=True, default = None)
        home_cat        = models.IntegerField(max_length=2, default=0)
        away_cat        = models.IntegerField(max_length=2, default=0)

        def __unicode__(self):
                return "%s v. %s" % (self.home_player.name, self.away_player.name)

class Activation(models.Model):
        week            = models.ForeignKey(Week)
        skater          = models.ForeignKey(Skater)
        player          = models.ForeignKey(Player)
	bench		= models.BooleanField()

class Activated_Team(models.Model):
        skater          = models.ForeignKey(Skater)
        player          = models.ForeignKey(Player)

