from django.db import models

class Hockey_Team(models.Model):
        name            = models.CharField(max_length=3)
        full_name       = models.CharField(max_length=24)

        def __unicode__(self):
                return self.name

class Skater(models.Model):
        nhl_id          = models.IntegerField(max_length=8)
        name            = models.CharField(max_length=64, default="")
        hockey_team     = models.ForeignKey(Hockey_Team, default=0)
        position        = models.CharField(max_length=2, default="")
        games           = models.IntegerField(max_length=8, default=0)
        goals           = models.IntegerField(max_length=8, default=0)
        assists         = models.IntegerField(max_length=8, default=0)
        points          = models.IntegerField(max_length=8, default=0)
        plus_minus      = models.IntegerField(max_length=4, default=0)
        shg             = models.IntegerField(max_length=8, default=0)
        sha             = models.IntegerField(max_length=8, default=0)
        ppg             = models.IntegerField(max_length=8, default=0)
        ppa             = models.IntegerField(max_length=8, default=0)
        gwg             = models.IntegerField(max_length=8, default=0)
        psg             = models.IntegerField(max_length=8, default=0)
        pims            = models.IntegerField(max_length=8, default=0)
        hits            = models.IntegerField(max_length=8, default=0)
        shots           = models.IntegerField(max_length=8, default=0)
        blocks          = models.IntegerField(max_length=8, default=0)
        fights          = models.IntegerField(max_length=8, default=0)
        giveaways       = models.IntegerField(max_length=8, default=0)
        takeaways       = models.IntegerField(max_length=8, default=0)
        faceoff_win     = models.IntegerField(max_length=8, default=0)
        faceoff_loss    = models.IntegerField(max_length=8, default=0)
        shootout_made   = models.IntegerField(max_length=8, default=0)
        shootout_fail   = models.IntegerField(max_length=8, default=0)
        wins            = models.IntegerField(max_length=8, default=0)
        otloss          = models.IntegerField(max_length=8, default=0)
        shutouts        = models.IntegerField(max_length=8, default=0)
        penshot_save    = models.IntegerField(max_length=8, default=0)
        penshot_ga      = models.IntegerField(max_length=8, default=0)
        shootout_save   = models.IntegerField(max_length=8, default=0)
        shootout_ga     = models.IntegerField(max_length=8, default=0)
        saves           = models.IntegerField(max_length=8, default=0)
        goals_against   = models.IntegerField(max_length=8, default=0)
        fantasy_points  = models.IntegerField(max_length=8, default=0)

	def __unicode__(self):
		return self.name

class Week(models.Model):
        number          = models.IntegerField(max_length=2)

        def __unicode__(self):
                return "Week: %s" % self.number

class Player(models.Model):
        name            = models.CharField(max_length=32)
        conference      = models.CharField(max_length=4, default ="")

        def __unicode__(self):
                return self.name

class Team(models.Model):
        skater          = models.ForeignKey(Skater)
        player          = models.ForeignKey(Player)
        week            = models.IntegerField(max_length=2)
        active          = models.IntegerField(max_length=1)

class Point(models.Model):
        skater                  = models.ForeignKey(Skater)
        week                    = models.ForeignKey(Week)
        fantasy_points          = models.IntegerField(max_length=4)
        goals                   = models.IntegerField(max_length=4)
        assists                 = models.IntegerField(max_length=4)
        shootout                = models.IntegerField(max_length=4)
        plus_minus              = models.IntegerField(max_length=4)
        offensive_special       = models.IntegerField(max_length=4)
        true_grit_special       = models.IntegerField(max_length=4)
        goalie                  = models.IntegerField(max_length=4)
        date                    = models.DateField()

class Team_Point(models.Model):
        point           = models.ForeignKey(Point)
        player          = models.ForeignKey(Player)

class Injury(models.Model):
        skater          = models.ForeignKey(Skater)
        date            = models.DateField()
        name            = models.CharField(max_length=128)
        status          = models.CharField(max_length=128)
        description     = models.CharField(max_length=512)


class Post(models.Model):
        title           = models.CharField(max_length=256)
        text            = models.CharField(max_length=128000)

class Week_Dates(models.Model):
        week            = models.ForeignKey(Week)
        date            = models.DateField()

class Pool(models.Model):
        name = models.CharField(max_length="64", default="")
        current_week = models.ForeignKey(Week)

