from django.db import models
from django.db.models import Count
from hockeypool.models import *

class Forum(models.Model):
        title           = models.CharField(max_length=64, default="Nothing to see here folks")
        description     = models.CharField(max_length=256, default="No, seriously, nothing")
        type            = models.IntegerField(max_length=1, default=1)

        def __unicode__(self):
                return self.title

        def get_threads(self):
                return(Thread.objects.filter(forum_id = self.id).count())

        def get_posts(self):
                return(Thread_Post.objects.filter(thread__forum_id = self.id).count())

        def get_last_poster(self):
                t = Thread_Post.objects.filter(thread__forum_id = self.id).latest('created')
                return(t.creator)

        def get_last_poster_time(self):
                t = Thread_Post.objects.filter(thread__forum_id = self.id).latest('created')
                return(t.created)

class Thread(models.Model):
        forum           = models.ForeignKey(Forum)
        creator         = models.ForeignKey(Player)
        title           = models.CharField(max_length=128, default="I'm stupid and forgot to make a title")
        created         = models.DateTimeField(auto_now_add=True)
        views           = models.IntegerField(max_length=10, default=0)

        def __unicode__(self):
                return unicode(self.creator) + " - " + self.title

        def get_posts(self):
                return (Thread_Post.objects.filter(thread = self.id).count())

        def get_last_poster(self):
                t = Thread_Post.objects.filter(thread = self.id).latest('created')
                return(t.creator)

        def get_last_poster_time(self):
                t = Thread_Post.objects.filter(thread = self.id).latest('created')
                return(t.created)

class Thread_Post(models.Model):
        creator         = models.ForeignKey(Player)
        created         = models.DateTimeField(auto_now_add=True)
        thread          = models.ForeignKey(Thread)
        body            = models.TextField(max_length=128000)

        def __unicode__(self):
                return u"%s - %s - %s" % (self.creator, self.thread, self.body)

