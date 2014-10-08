from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import F
from datetime import datetime, timedelta
from django.utils.timezone import utc

from forum.models import *
from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
        draft_picks = Draft_Pick.objects.all().order_by("id")
        if len(draft_picks) == 0:
                player_status = None
                status = Draft_Start.objects.all()
                for x in status:
                        if request.user.id == x.player.id:
                                player_status = x.status
                context = {'page_name' : "Draft", 'status' : 0, 'message' : "Not all players ready to start draft", 'statuses' : status, 'player_status' : player_status}
                return render(request, 'draft/index.html', context)
        else:
                null_count = Draft_Pick.objects.filter(pick__isnull=True).count()
                draft_picks = Draft_Pick.objects.all().order_by("id")
                total_picks = len(draft_picks)
                if null_count != 0:
                        now = datetime.utcnow().replace(tzinfo=utc)
			if total_picks - null_count - 1 >= 0:
				before = draft_picks[total_picks - null_count - 1].time
			else:
				before = now
                        end = before + timedelta(minutes=3, seconds=0) - timedelta(minutes=0,seconds=before.second)
                        time_diff = end - now
                        time_left = int(time_diff.total_seconds())
                        pick = draft_picks[0]

                        for x in draft_picks:
                                if x.pick == None:
                                        pick = x
                                        break

                        lw = []
                        c = []
                        rw = []
                        ld = []
                        rd = []
                        g = []

                        all_picks = Draft_Pick.objects.filter(pick__isnull=False)[:160]
                        for x in all_picks:
                                if x.player.id == request.user.id:
                                        if x.pick != None:
                                                if x.pick.position == "L":
                                                        lw.append(x.pick)
                                                elif x.pick.position == "C":
                                                        c.append(x.pick)
                                                elif x.pick.position == "R":
                                                        rw.append(x.pick)
                                                elif x.pick.position == "D":
                                                        if len(ld) <= len(rd):
                                                                ld.append(x.pick)
                                                        else:
                                                                rd.append(x.pick)
                                                elif x.pick.position == "G":
                                                        g.append(x.pick)

                        if pick.player.id == request.user.id:
                                is_turn = 1
                        else:
                                is_turn = 0

                        current_round = pick.round.id
                        order = []

                        for x in draft_picks:
                                if x.round.id == current_round:
                                        order.append(x)

                        top_picks_array = Skater.objects.exclude(id__in = Draft_Pick.objects.filter(pick__isnull=False).values_list("pick_id", flat=True)).exclude(position='G').order_by("-fantasy_points")[0:10]
                        top_picks = []
                        for x in top_picks_array:
                                        top_picks.append([x.nhl_id, x.name, x.position])

                        over = 0
                        context = {'page_name' : "Draft", "current_round" : pick.round.id, "is_turn" : is_turn, "round_order" : order, "top_picks" : top_picks, "time_left" : time_left, "lw" : lw, "c" : c, "rw" : rw, "ld" : ld, "rd" : rd, "g" : g, 'over' : over}
                else:
                        over = 1
                        context = {'page_name' : "Draft", 'over' : over}
                return render(request, 'draft/index.html', context)

@login_required
def draft_round(request, draft_round):
        num_picks = Draft_Pick.objects.all().count()
        if num_picks <= 0:
                context = {'page_name' : "Draft Round", 'round' : draft_round, "errors" : 1, "message" : "The draft has not yet started... you cannot yet view this page"}
                return render(request, 'hockeypool/draft_round.html', context)
        else:
                picks = Draft_Pick.objects.filter(round = draft_round)
                pick_order = []
                for x in picks:
                        pick_order.append(x.get_pick())
                context = {'page_name' : "Draft Round", 'round' : draft_round, "errors" : 0, "order" : pick_order}
                return render(request, 'draft/draft_round.html', context)

