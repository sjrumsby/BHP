from django.db import models
from hockeypool.models import *

class Waiver(models.Model):
        skater          = models.ForeignKey(Skater)
        player          = models.ForeignKey(Player)
        state           = models.IntegerField(default=0)

        def all_waiver_row(self):
                if self.state == 0:
                        status = "Pending"
                elif self.state == 1:
                        status = "Accepted"
                elif self.state == 2:
                        status = "Dropped"
                else:
                        status = "Finished"
                return "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (self.skater.first_name + ' ' + self.skater.last_name, self.skater.get_position(), self.player.name, status)

        def own_waiver_row(self):
                if self.state == 0:
                        status = "Pending"
                elif self.state == 1:
                        status = "Accepted"
                elif self.state == 2:
                        status = "Dropped"
                else:
                        status = "Finished"
                return '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href="/waivers/cancel/%s/">%s</a></td></tr>' % (self.skater.first_name + ' ' + self.skater.last_name, self.skater.get_position(), self.player.name, status, self.id, "Cancel")

        def __unicode__(self):
                return self.skater.name + " - " + self.player.name

class Waiver_Pickup(models.Model):
        skater          = models.ForeignKey(Skater)
        player          = models.ForeignKey(Player)
        state           = models.IntegerField(default=0)

