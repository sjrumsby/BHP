from django.db import models
from hockeypool.models import *

class Power_Rank(models.Model):
        week            = models.IntegerField(max_length=2)
        player          = models.ForeignKey(Player)
        power_rank      = models.IntegerField(max_length=2)
        comment         = models.CharField(max_length=4096)

