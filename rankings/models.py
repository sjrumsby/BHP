from django.db import models
from hockeypool.models import *

class Power_Rank(models.Model):
        week            = models.IntegerField()
        player          = models.ForeignKey(Player)
        power_rank      = models.IntegerField()
        comment         = models.CharField(max_length=4096)

