import json
from re import sub
from django.http import HttpResponse, HttpResponseRedirect
import datetime, time
from django.utils.timezone import utc
from django.core.cache import cache

from hockeypool.models import *
from match.models import *
from draft.models import *
import logging

logger = logging.getLogger(__name__)

def getPlayer(request, player_name):
        s = Skater.objects.filter(name__icontains=player_name)[:5]
        data = ""
        if len(s) >= 1:
                for i in s:
                        data = data + '<p><a onclick="replace_draft_text(\'%s\');" href="javascript:void(0)">%s</p>' % (i.name, i.name)
        else:
                data = "No results found"
        return HttpResponse(data)

def getWaiverPlayer(request, player_name):
        s = Skater.objects.filter(name__icontains=player_name)[:5]
        data = ""
        if len(s) >= 1:
                for i in s:
                        data = data + "<p><a onclick=\"replace_waiver_text('%s', '%s');\" href=\"javascript:void(0)\">%s</p>" % (i.name.replace("'", "\\'"), i.nhl_id, i.name)
        else:
                data = "No results found"
        return HttpResponse(data)

def getTradeOwn(request, player_name):
        s = Skater.objects.filter(name__icontains=player_name)[:5]
        data = ""
        if len(s) >= 1:
                for i in s:
                        data = data + '<p><a onclick="replace_trade_own_text(\'%s\');" href="javascript:void(0)">%s</p>' % (i.name, i.name)
        else:
                data = "No results found"
        return HttpResponse(data)

def getTradeOther(request, player_name):
        s = Skater.objects.filter(name__icontains=player_name)[:5]
        data = ""
        if len(s) >= 1:
                for i in s:
                        data = data + '<p><a onclick="replace_trade_other_text(\'%s\');" href="javascript:void(0)">%s</p>' % (i.name, i.name)
        else:
                data = "No results found"
        return HttpResponse(data)

def draftUpdate(request):
        check_draft = Draft_Pick.objects.all().count()

        if check_draft > 0:
                null_picks = Draft_Pick.objects.filter(pick__isnull=True).order_by("id")
                null_count = len(null_picks)
                draft_picks = Draft_Pick.objects.select_related().all().order_by("id")
                total_picks = len(draft_picks)

                if null_count != 0:
                        now = datetime.datetime.utcnow().replace(tzinfo=utc)
                        if Draft_Swap.objects.filter(pick = draft_picks[total_picks - null_count]).exists():
                                draft_swap = Draft_Swap.objects.filter(pick = draft_picks[total_picks - null_count]).order_by("-id")[0]
                                before = draft_swap.time
                        else:
				if total_picks - null_count - 1 >= 0:
					before = draft_picks[total_picks - null_count - 1].time
				else:
					before = now

                        end = before + datetime.timedelta(minutes=3, seconds=0) - datetime.timedelta(minutes=0,seconds=before.second)
                        time_diff = end - now
                        time_left = int(time_diff.total_seconds())
                        state = "draft"
                        round_picks = []
                        round_order = []
                        top_picks = []
                        lw = []
                        c = []
                        rw = []
                        ld = []
                        rd = []
                        g = []

                        all_picks = Draft_Pick.objects.select_related().filter(pick__isnull=False).filter(player=request.user)

                        for x in all_picks:
                                if x.pick.position[0] == "L":
                                        lw.append(x.pick.name + " (" + x.pick.position + ")")
                                elif x.pick.position[0] == "C":
                                        c.append(x.pick.name + " (" + x.pick.position + ")")
                                elif x.pick.position[0] == "R":
                                        rw.append(x.pick.name + " (" + x.pick.position + ")")
                                elif x.pick.position[0] == "D" and (len(ld) <= len(rd)):
                                        ld.append(x.pick.name + " (" + x.pick.position + ")")
                                elif x.pick.position[0] == "D":
                                        rd.append(x.pick.name + " (" + x.pick.position + ")")
                                elif x.pick.position[0] == "G":
                                        g.append(x.pick.name + " (" + x.pick.position + ")")

                        for x in null_picks:
                                if x.pick == None:
                                        next_pick = x
                                        current_round = x.round.number
                                        break

                        for x in draft_picks:
                                if x.round.number == current_round:
                                        round_picks.append(x)

                        for x in round_picks:
                                if x.pick == None:
                                        round_order.append(x.player.name)
                                else:
                                        round_order.append("%s - %s" % (x.player.name, x.pick.name))
                        top_picks_array = cache.get('top_picks')
                        if top_picks_array is None:
                                top_picks_array = Skater.objects.exclude(id__in = Draft_Pick.objects.filter(pick__isnull=False).values_list("pick_id", flat=True)).exclude(position='G').order_by("-fantasy_points")[0:10]
                                cache.set('top_picks', top_picks_array, 10)

                        for x in top_picks_array:
                                top_picks.append([x.nhl_id, x.name, x.position])

                        if next_pick.player.id == request.user.id:
                                is_turn = 1
                        else:
                                is_turn = 0

                        response_data = {'state' : state, 'time_left' : time_left, 'current_round' : current_round, 'round_order' : round_order, 'current_pick' : next_pick.get_pick(), "top_picks" : top_picks, "is_turn" : is_turn, "lw" : lw, "c" : c, "rw" : rw, "ld" : ld, "rd" : rd, "g" : g }
                else:
                        response_data = {'state' : 'finished'}
        else:
                ready_check = Draft_Start.objects.filter(status=0).count()
                if ready_check > 0:
                        ready_status = Draft_Start.objects.all()
                        draft_ready = []
                        for x in ready_status:
                                temp_arr = [x.status, x.player.name]
                                draft_ready.append(temp_arr)
                        response_data = {"state" : "ready", "player_status" : draft_ready}
                else:
                         response_data = {"state" : "ready_start"}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def pick_player(request):
        if request.method == "POST":
                player = request.POST.get("player_name")
                if Skater.objects.filter(name__exact = player).exists():
                        draft_picks = Draft_Pick.objects.all().order_by("id")
                        check = 1
                        for x in draft_picks:
                                if x.pick == None:
                                        current_pick = x
                                        break
                                else:
                                        if x.pick.name == player:
                                                check = 0
                                                break
                        if check == 0:
                                data = {"errors" : 1, "message" : "Player already been drafted"}
                        else:
                                if x.player.id == request.user.id:
                                        save_pick = Skater.objects.filter(name__exact = player)
                                        current_pick.pick = save_pick[0]
                                        current_pick.time = datetime.datetime.now()
                                        current_pick.save()
                                        data = {"errors" : 0, "message" : "Player successfully drafted."}
                                else:
                                        data = {"errors" : 1, "message" : "Not your turn to pick"}
                else:
                        data = {"errors" : 1, "message" : "Player does not exists"}
        else:
                data = {"errors" : 1, "message" : "Did not POST any/correct data"}
        return HttpResponse(json.dumps(data), content_type="application/json")

def updateStatus(request):
        if request.method == "POST":
                ready_status = request.POST.get("status")
                draft_start = Draft_Start.objects.filter(player = request.user)[0]
                draft_start.status = ready_status
                draft_start.save()
                errors = 0
        else:
                errors = 1
        data = {"errors" : errors}
        return HttpResponse(json.dumps(data), content_type="application/json")

def activateRoster(request):
        activations = json.loads(request.body)
        logger.info("User: %s Attempting to activate: %s" % (request.user.id, activations))
        team_check = 1
	vals = []
        error = 0
        msg = []
        p = Pool.objects.get(pk=1)
        current_week = p.current_week
        week = Week.objects.get(number = current_week.number + 1)
        date = datetime.datetime.now()
        formed_date = "%s-%s-%s" % (date.year, str(date.month).zfill(2), str(date.day).zfill(2))

        logger.info("Activation process date for user: %s: %s" % (request.user.id, formed_date))
        Activation.objects.filter(player__id = request.user.id).delete()
        team_to_activate = []

        for x in activations['ids']:
                if x['id'].isdigit():
                        if Team.objects.filter(player__id = request.user.id, skater__nhl_id = x['id']).count() == 1:
                                t = Team.objects.get(player__id = request.user.id, skater__nhl_id = x['id'])
				if x['position'] not in t.skater.position and x['position'] != 'B':
					logger.info("Can not activate %s as position %s" % (t.skater, x['position']))
					error = 1
				else:
					team_to_activate.append([t.skater, t.player, x['position']])
                        else:
				error = 1
                                logger.info("Skater not found with id: %s" % x['id'])

	if error != 1:
		c = l = r = d = g = b = 0
		for x in team_to_activate:
			if x[2] == "C":
				c = c + 1
			elif x[2] == "L":
				l = l + 1
			elif x[2] == "R":
				r = r + 1
			elif x[2] == "D":
				d = d + 1
			elif x[2] == "G":
				g = g + 1
			elif x[2] == "B":
				b = b + 1
		if c < 3:
			error = 2
			msg.append("Too few centres")
		if l < 3:
			error = 2
			msg.append("Too few Left Wing")
		if r < 3:
			error = 2
			msg.append("Too few Right Wing")
		if d < 6:
			error = 2
			msg.append("Too few defense")
		if g < 1:
			error = 2
			msg.append("Too few goalies")
		if c > 3:
			error = 1
			msg.append("Too many centres")
		if l > 3:
			error = 1
			msg.append("Too many Left Wing")
		if r > 3:
			error = 1
			msg.append("Too many Right Wing")
		if d > 6:
			error = 1
			msg.append("Too many defense")
		if g > 1:
			error = 1
			msg.append("Too many goaies")

		if b > 1:
			error = 1
			msg.append("Too many benches")

        if error != 1:
		Activation.objects.filter(player_id=request.user.id).delete()
                for t in team_to_activate:
			if t[2] == 'B':
				a = Activation.objects.create(skater=t[0], player=t[1], week=week, position=t[2])
				a.save()
			else:
				a = Activation.objects.create(skater=t[0], player=t[1], week=week, position=t[2])
				a.save()
                        logger.info("Skater: %s, position: %s" % (a.skater.name, a.position))

        data = {"error" : error, "message" : msg}
        return HttpResponse(json.dumps(data), content_type="application/json")

def tradePlayer(request):
        own_player = request.POST.get("own_player")
        other_player = request.POST.get("other_player")
        if Team.objects.filter(skater__name = own_player).exists():
                own_skater = Team.objects.filter(skater__name = own_player)[0]
                if Team.objects.filter(skater__name = other_player).exists():
                        other_skater = Team.objects.filter(skater__name = other_player)[0]
                        logger.info("%s is attempting to trade %s for %s from another player" % (request.user, own_skater.skater.name, other_skater.skater.name))
                        date = datetime.datetime.utcnow()
                        if date.year == 2013 and date.month < 8:
                                weekdate = Week_Dates.objects.get(date = "2013-10-01")
                        else:
                                formed_date = "%s-%s-%s" % (date.year, str(date.month).zfill(2), str(date.day).zfill(2))
                                weekdate = Week_Dates.objects.get(date = formed_date)
                        Trade.objects.create(player1 = own_skater.player, player2 = other_skater.player, skater1 = own_skater.skater, skater2 = other_skater.skater, week = weekdate.week, state=0)
                        error = 0
                        msg = "Trade initiated. Waiting on other player to confirm/deny"
                else:
                        error = 1
                        msg = "No GM owns the other player... cannot initiate trade"
        else:
                error = 1
                msg = "You do not own the player you are trying to trade"
        data = { "error" : error, "msg" : msg }
        return HttpResponse(json.dumps(data), content_type="application/json")

