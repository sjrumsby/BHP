from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import F

from forum.models import *
from hockeypool.models import *

import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
        forum = Forum.objects.all()
        forum_general = []
        forum_matches = []
        forum_features = []
        for f in forum:
                if f.type == 1:
                        forum_general.append(f)
                elif f.type == 2:
                        forum_matches.append(f)
                elif f.type == 3:
                        forum_features.append(f)
        context = {'page_name' : 'Forum', 'forum_general' : forum_general, 'forum_matches' : forum_matches, 'forum_features' : forum_features}
        return render(request, 'forum/index.html', context)

@login_required
def forum_detail(request, forum_id):
        forum = Forum.objects.filter(id = forum_id)
        forum = forum[0]
        threads = Thread.objects.filter(forum_id = forum_id)
        context = {'page_name' : forum.title, 'threads' : threads, 'forum_id' : forum_id}
        return render(request, 'forum/forum_detail.html', context)

@login_required
def forum_newthread(request, forum_id):
        forum = Forum.objects.filter(id = forum_id)
        forum = forum[0]
        if request.method == "POST":
                title = request.POST.get('newthread_subject')
                comment = request.POST.get('newthread_post')
                player = Player.objects.get(id=request.user.id)
                thread = Thread.objects.create(forum_id = forum_id, creator = player, title = title)
                post = Thread_Post.objects.create(creator_id = player.id, thread_id = thread.id, body = comment)
                return HttpResponseRedirect("/forum/" + forum_id)
        context = {'page_name' : forum.title, 'forum_id' : forum_id}
        return render(request, 'forum/forum_newthread.html', context)

@login_required
def forum_thread(request, thread_id):
        thread = Thread.objects.filter(id = thread_id)[0]
        if request.method == "POST":
                if (request.POST.get('newthread_post') != None):
                        comment = request.POST.get('newthread_post')
                        player = Player.objects.get(id=request.user.id)
                        post = Thread_Post.objects.create(creator_id = player.id, thread_id = thread.id, body = comment)
                        return HttpResponseRedirect("/forum/thread/" + thread_id)
        Thread.objects.filter(id = thread_id).update(views = F("views") + 1)
        posts = Thread_Post.objects.filter(thread = thread_id)[:20]
        context = {'page_name' : thread.title, 'thread' : thread, 'posts' : posts, 'offset' : 0}
        return render(request, 'forum/forum_thread.html', context)

@login_required
def forum_thread_reply(request, thread_id):
        thread = Thread.objects.filter(id = thread_id)[0]
        if request.method == "POST":
                comment = request.POST.get('newthread_post')
                player = Player.objects.get(id=request.user.id)
                post = Thread_Post.objects.create(creator_id = player.id, thread_id = thread.id, body = comment)
                return HttpResponseRedirect("/forum/thread/" + thread_id)
        context = {'page_name' : thread.title + " - Reply"}
        return render(request, "forum/forum_thread_reply.html", context)

