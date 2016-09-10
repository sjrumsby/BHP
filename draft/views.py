from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import F
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.db.models import Sum

from hockeypool.models import *
from draft.models import *

import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
	p = Pool.objects.get(id=1)
        draft_picks = Draft_Pick.objects.filter(round__year_id=p.current_year_id).order_by("id")
        if len(draft_picks) == 0:
                player_status = None
                status = Draft_Start.objects.all()
                for x in status:
                        if request.user.id == x.player.id:
                                player_status = x.status
                context = {'page_name' : "Draft", 'status' : 0, 'message' : "Not all players ready to start draft", 'statuses' : status, 'player_status' : player_status}
                return render(request, 'draft/index.html', context)
        else:
                null_count = Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=True).count()
                draft_picks = Draft_Pick.objects.filter(round__year_id=p.current_year_id).order_by("id")
                total_picks = len(draft_picks)
                if null_count != 0:
                        now = datetime.datetime.utcnow().replace(tzinfo=utc)
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

                        all_picks = Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False)[:168]
                        for x in all_picks:
                                if x.player.id == request.user.id:
                                        if x.pick != None:
                                                if "L" in x.pick.get_position():
                                                        lw.append(x.pick)
                                                elif "C" in x.pick.get_position():
                                                        c.append(x.pick)
                                                elif "R" in x.pick.get_position():
                                                        rw.append(x.pick)
                                                elif "D" in x.pick.get_position():
                                                        if len(ld) <= len(rd):
                                                                ld.append(x.pick)
                                                        else:
                                                                rd.append(x.pick)
                                                elif "G" in x.pick.get_position():
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

			tops = Skater.objects.filter(nhl_id__in=Point.objects.filter(game__year_id=1).values('skater_id').annotate(fp=Sum('fantasy_points')).order_by("-fp")[0:10].values_list("skater_id", flat=True))
			top_picks = []

			for t in top_picks:
				top_picks.append(t.__str__)

			logger.info(top_picks)

                        over = 0
                        context = {'page_name' : "Draft", "current_round" : pick.round.number, "is_turn" : is_turn, "round_order" : order, "top_picks" : top_picks, "time_left" : time_left, "lw" : lw, "c" : c, "rw" : rw, "ld" : ld, "rd" : rd, "g" : g, 'over' : over}
                else:
                        over = 1
                        context = {'page_name' : "Draft", 'over' : over}
                return render(request, 'draft/index.html', context)

@login_required
def draft_round(request, draft_round):
        num_picks = Draft_Pick.objects.filter(round__year_id=2).count()
        if num_picks <= 0:
                context = {'page_name' : "Draft Round", 'round' : draft_round, "errors" : 1, "message" : "The draft has not yet started... you cannot yet view this page"}
                return render(request, 'hockeypool/draft_round.html', context)
        else:
                picks = Draft_Pick.objects.filter(number__in=[8*(int(draft_round) - 1) + i for i in range(1,9)]).filter(round__year_id=2).order_by("id")
                pick_order = []
                for x in picks:
                        pick_order.append({"manager" : x.player, "skater" : x.pick})
                context = {'page_name' : "Draft Round", 'round' : draft_round, "errors" : 0, "order" : pick_order}
                return render(request, 'draft/draft_round.html', context)

