from django.db import models

class Trade(models.Model):
        player1         = models.ForeignKey(Player, related_name="player1")
        player2         = models.ForeignKey(Player, related_name="player2")
        skater1         = models.ForeignKey(Skater, related_name="skater1")
        skater2         = models.ForeignKey(Skater, related_name="skater2")
        week            = models.ForeignKey(Week)
        state           = models.IntegerField(max_length=1, default=0)

