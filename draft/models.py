from django.db import models
from django.db.models import Count
from hockeypool.models import *

class Draft_Round(models.Model):
        number 	= models.IntegerField(default=1)
	year 	= models.ForeignKey(Year)

        def __unicode__(self):
                return self.number

class Draft_Pick(models.Model):
        round = models.ForeignKey(Draft_Round)
        player = models.ForeignKey(Player)
        pick = models.ForeignKey(Skater, blank=True, null=True)
        time = models.DateTimeField(blank=True, null=True)
	number = models.IntegerField(blank=True, null=True)

        def get_round(self):
                return self.round.number

        def get_pick(self):
                if self.pick == None:
                        str = self.player.name
                else:
                        str = "%s - %s" % (self.player.name, self.pick.first_name + " " + self.pick.last_name)
                return str

class Draft_Start(models.Model):
        player = models.ForeignKey(Player)
        status = models.IntegerField(default=0)

class Draft_Swap(models.Model):
        round = models.ForeignKey(Draft_Round)
        time = models.DateTimeField(blank=True, null=True)
        pick = models.ForeignKey(Draft_Pick)
