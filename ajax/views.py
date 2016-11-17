import json
from re import sub
from django.http import HttpResponse, HttpResponseRedirect
import datetime, time
from django.utils.timezone import utc
from django.core.cache import cache

from hockeypool.models import *
from match.models import *
from draft.models import *
from trades.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Sum, Q
import logging

logger = logging.getLogger(__name__)

def getPlayer(request):
	player_name = request.POST.get("player_name", False)
	if player_name:
		s1 = Skater.objects.filter(full_name__icontains=player_name)[:5]
		data = ""
		if len(s1) >= 1:
			for i in s1:
				data = data + '<p><a onclick="replace_draft_text(\'%s\', %s);" href="javascript:void(0)">%s</p>' % (i.first_name + " " + i.last_name, i.nhl_id, i.first_name + " " + i.last_name)
		else:
			data = "No results found"

		return HttpResponse(data)
	else:
		return HttpResponse("No data found");

def getPlayerPopup(request, playerID):
	p = Player.objects.get(id=playerID)
	c = p.get_player_popup_data()
	pool = Pool.objects.get(pk=1)

	picks = Draft_Pick.objects.filter(player=p).filter(pick__isnull=False).order_by("-time")[0:5]

	matches = Match.objects.select_related().filter(Q(home_player_id=p.id)|Q(away_player_id=p.id)).filter(week__number__gt=pool.current_week.number)

	response_data = {
		'name': p.name,
		'record': {
			'wins': 0,
			'losses': 0
		},
		'current_week': {
			'vs': 'Someone',
			'location': '',
			'scores': {
				'home': {
					'fp': 0
				},
				'away': {
					'fp': 0
				}
			}
		},
		'upcoming_weeks': [],
		'picks': []
	}

	for p in picks:
		response_data['picks'].append({"name": p.pick.full_name})

	for m in matches[:3]:
		tmpMatch = {}
		if m.home_player_id == p.id:
			tmpMatch['vs'] = m.away_player.name
		else:
			tmpMatch['vs'] = m.home_player.name
		tmpMatch['week'] = m.week.number
		response_data['upcoming_weeks'].append(tmpMatch)

	if pool.current_week.number == 0:
		response_data['current_week']['vs'] = 'No match this week'

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def getSkater(request, nhlID):
	s = Skater.objects.get(nhl_id=nhlID)
	c = s.get_skater_category_data()
	pool = Pool.objects.get(pk=1)

	games = Game.objects.filter(date__gt=datetime.datetime.now()).filter(Q(home_team=s.hockey_team)|Q(away_team=s.hockey_team))
	upcomingGames = []

	for g in games:
		if g.home_team_id == s.hockey_team:
			opponent = g.away_team
		else:
			opponent = g.home_team
		upcomingGames.append({'opponent': opponent.name, 'date': g.date.strftime('%Y-%m-%d'), 'week': 1})
		if len(upcomingGames) >= 5:
			break

	response_data = {
		'categories': {
			'fantasy_points': c['categories']['fantasy_points'],
			'goals': c['categories']['goals'],
			'assists': c['categories']['assists'],
			'plus_minus': c['categories']['plus_minus'],
			'specialty': c['categories']['specialty'],
			'true_grit': c['categories']['true_grit'],
			'goalie': c['categories']['goalie'],
			'shootout': c['categories']['shootout']
		},
		'nhl_id': s.nhl_id,
		'name': s.get_name(),
		'games': s.games_played,
		'owner': s.get_owner(),
		'position': s.get_position(),
		'team': s.hockey_team.name,
		'upcomingGames': upcomingGames
	}

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def getWaiverPlayer(request, player_name):
        s1 = Skater.objects.filter(full_name__icontains=player_name)[:5]
        data = ""
        if len(s1) >= 1:
                for i in s1:
                        data = data + "<p><a onclick=\"replace_waiver_text('%s', '%s');\" href=\"javascript:void(0)\">%s</p>" % (i.first_name.replace("'", "\\'") + " " + i.last_name.replace("'", "\\'"), i.nhl_id, i.first_name + " " + i.last_name)
        else:
                data = "No results found"
        return HttpResponse(data)

def getTradeOwn(request, player_name):
        s = Skater.objects.filter(full_name__icontains=player_name)[:5]
        data = ""
        if len(s) >= 1:
                for i in s:
                        data = data + '<p><a onclick="replace_trade_own_text(\'%s\', \'%s\');" href="javascript:void(0)">%s</p>' % (i.first_name.replace("'", "\\'") + " " + i.last_name.replace("'", "\\'"), i.nhl_id, i.first_name + " " + i.last_name)
        else:
                data = "No results found"
        return HttpResponse(data)

def getTradeOther(request, player_name):
        s = Skater.objects.filter(full_name__icontains=player_name)[:5]
        data = ""
        if len(s) >= 1:
                for i in s:
                        data = data + '<p><a onclick="replace_trade_other_text(\'%s\', \'%s\');" href="javascript:void(0)">%s</p>' % (i.first_name.replace("'", "\\'") + " " + i.last_name.replace("'", "\\'"), i.nhl_id, i.first_name + " " + i.last_name)
        else:
                data = "No results found"
        return HttpResponse(data)

def draftUpdate(request):
	p = Pool.objects.get(id=1)
        check_draft = Draft_Pick.objects.filter(round__year_id=p.current_year_id).count()

        if check_draft > 0:
                null_picks = Draft_Pick.objects.select_related().filter(round__year_id=p.current_year_id).filter(pick__isnull=True).order_by("id")
                not_null_picks = Draft_Pick.objects.select_related().filter(round__year_id=p.current_year_id).filter(pick__isnull=False).order_by("id")
                null_count = len(null_picks)
                draft_picks = Draft_Pick.objects.select_related().filter(round__year_id=p.current_year_id).order_by("id")
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

                        all_picks = Draft_Pick.objects.select_related().filter(pick__isnull=False).filter(player=request.user.id).filter(round__year_id=p.current_year_id)

                        for x in all_picks:
                                if "L" in x.pick.get_position():
                                        lw.append({"name" : x.pick.get_draft_name()})
                                elif "C" in x.pick.get_position():
                                        c.append({"name" : x.pick.get_draft_name()})
                                elif "R" in x.pick.get_position():
                                        rw.append({"name" : x.pick.get_draft_name()})
                                elif "D" in x.pick.get_position():
                                        rd.append({"name" : x.pick.get_draft_name()})
                                elif "G" in x.pick.get_position():
                                        g.append({"name" : x.pick.get_draft_name()})

                        current_round = null_picks[0].round.number
			current_round_picks = draft_picks.filter(round__number=current_round)
			round_picks = []

                        for x in current_round_picks: 
				if x.pick is None:
					round_picks.append({"player" : x.player.name, "pick" : "None", "id" : x.player.id})
				else:
					round_picks.append({"player" : x.player.name, "pick" : x.pick.full_name, "id" : x.player.id})

			try:
				undrafted_sort = request.POST["undrafted_sort"]
			except MultiValueDictKeyError :
				undrafted_sort = "fantasy_points"

			try:
				undrafted_position = request.POST["undrafted_position"]
			except MultiValueDictKeyError :
				undrafted_position = "C"

			if undrafted_sort == "goals":
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).filter(game__year_id=1).values('skater_id').annotate(goals=Sum('goals')).order_by("-goals")[0:100].values_list("skater_id", flat=True))
			elif undrafted_sort == "assists":
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).filter(game__year_id=2).values('skater_id').annotate(assists=Sum('assists')).order_by("-assists")[0:100].values_list("skater_id", flat=True))
			elif undrafted_sort == "plus_minus":
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).filter(game__year_id=2).values('skater_id').annotate(plus_minus=Sum('plus_minus')).order_by("-plus_minus")[0:100].values_list("skater_id", flat=True))
			elif undrafted_sort == "offensive_special":
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).filter(game__year_id=2).values('skater_id').annotate(offensive_special=Sum('offensive_special')).order_by("-offensive_special")[0:100].values_list("skater_id", flat=True))
			elif undrafted_sort == "true_grit":
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).filter(game__year_id=2).values('skater_id').annotate(true_grit=Sum('true_grit_special')).order_by("-true_grit")[0:100].values_list("skater_id", flat=True))
			elif undrafted_sort == "goalie":
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).filter(game__year_id=2).values('skater_id').annotate(goalie=Sum('goalie')).order_by("-goalie")[0:100].values_list("skater_id", flat=True))
			elif undrafted_sort == "shootout":
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).exclude(skater_id__in=Skater_Position.objects.filter(position_id=Position.objects.get(code="G")).values_list("skater_id", flat=True)).filter(game__year_id=2).values('skater_id').annotate(shootout=Sum('shootout')).order_by("-shootout")[0:100].values_list("skater_id", flat=True))
			else:
				top_picks_array = Skater.objects.filter(nhl_id__in=Point.objects.exclude(skater_id__in=Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=False).values_list("pick_id", flat=True)).filter(game__year_id=2).values('skater_id').annotate(fantasy_points=Sum('fantasy_points')).order_by("-fantasy_points")[0:100].values_list("skater_id", flat=True))

                        for x in top_picks_array:
				if len(top_picks) <= 8:
					if undrafted_position in x.get_position():
						top_picks.append({"name" : x.full_name, "position" : x.get_position(), "id" : x.nhl_id})

                        if null_picks[0].player.id == request.user.id:
                                is_turn = 1
                        else:
                                is_turn = 0

                        response_data = {'state' : state, 'time_left' : time_left, 'current_round' : current_round, 'round_order' : round_picks, 'current_pick' : null_picks[0].get_pick(), "top_picks" : top_picks, "is_turn" : is_turn, "lw" : lw, "c" : c, "rw" : rw, "ld" : ld, "rd" : rd, "g" : g }
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
	p = Pool.objects.get(id=1)
        if request.method == "POST":
                player_id = request.POST.get("player_id")
                if Skater.objects.filter(nhl_id = player_id).exists():
			s = Skater.objects.get(nhl_id=player_id)
			current_pick = Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick__isnull=True).order_by("id")[0]


			check = Draft_Pick.objects.filter(round__year_id=p.current_year_id).filter(pick_id=player_id).count()
                        if check == 1:
                                data = {"errors" : 1, "message" : "Player already been drafted"}
                        else:
                                if current_pick.player_id == request.user.id:
					current_pick.pick = s
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
                draft_start = Draft_Start.objects.filter(player = request.user.id)[0]
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
        week = Week.objects.filter(number = p.current_week.number).filter(year_id = p.current_year_id)[0]
        date = datetime.datetime.now()
        formed_date = "%s-%s-%s" % (date.year, str(date.month).zfill(2), str(date.day).zfill(2))

        logger.info("Activation process date for user: %s: %s" % (request.user.id, formed_date))
        Activation.objects.filter(player__id = request.user.id).delete()
        team_to_activate = []

        for x in activations['ids']:
                if x['id'].isdigit():
                        if Team.objects.filter(player__id = request.user.id, skater__nhl_id = x['id']).count() == 1:
                                t = Team.objects.get(player__id = request.user.id, skater__nhl_id = x['id'])
				if x['position'] not in t.skater.get_position() and x['position'] != 'B':
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
		if g < 2:
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
		if g > 2:
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
                        logger.info("Skater: %s, position: %s" % (a.skater.first_name+ ' ' + a.skater.last_name, a.position))

        data = {"error" : error, "message" : msg}
        return HttpResponse(json.dumps(data), content_type="application/json")

def tradePlayer(request):
        own_player = request.POST.get("own_player")
        other_player = request.POST.get("other_player")
	pool = Pool.objects.get(pk=1)
	logger.info("%s is trying to trade %s for %s" % (request.user.id, own_player, other_player))
	error = 0

	try:
		own_skater = Team.objects.get(skater_id=own_player, player_id=request.user.id)
	except Team.DoesNotExist:
		error = 1
		data = {"error" : 1, "msg" : "You do not own the player you are trying to tade"}

	try:
		 other_skater = Team.objects.get(skater_id=other_player)
	except Team.DoesNotExist:
		error = 1
                data = {"error" : 1, "msg" : "The player you are trading for is not owned"}

	if other_skater.player_id == request.user.id:
		error = 1
		data = {"error" : 1, "msg" : "You cannot trade for your own player"}

	if error == 0:
		Trade.objects.create(player1 = own_skater.player, player2 = other_skater.player, skater1 = own_skater.skater, skater2 = other_skater.skater, week = pool.current_week, state=0)
		msg = "Trade initiated. Waiting on other player to confirm/deny"
		data = { "error" : error, "msg" : msg }

        return HttpResponse(json.dumps(data), content_type="application/json")

def updateTheme(request):
	data = json.loads(request.body)
	newTheme = data["new_theme"]

	if newTheme is not None:
		p = Player.objects.get(id=request.user.id)
		p.theme = newTheme
		p.save()
                error = 0
                msg = "Successfully updated theme"
	else:
		error = 1
		msg = "Theme cannot be empty"

        data = { "error" : error, "msg" : msg }
        return HttpResponse(json.dumps(data), content_type="application/json")

def changePassword(request):
	user = User.objects.get(id=request.user.id)
	data = json.loads(request.body)
	old_pass = data["old_pass"]
	password1 = data["password1"]
	password2 = data["password2"]

	if password1 != "" and old_pass != "" and password1 == password2:
		logger.info("Attempting password reset for user: %s" % request.user)
		if user.check_password(old_pass):
			hash_pass = make_password(password1)
			user.password = hash_pass
			user.save()
			logger.info("Successfully changed password")
			error = 0
			msg = "Successfully changed password"
		else:
			logger.info("Failure: old password did not match")
			error = 1
			msg = "Incorrect current password"
	else:
		error = 1
		msg = "Old password and both new passwords must not be empty"
	
        data = { "error" : error, "msg" : msg }
        return HttpResponse(json.dumps(data), content_type="application/json")

def updateTeamName(request):
	data = json.loads(request.body)
	newTeamName = data["new_team_name"]
	logger.info(newTeamName)
	logger.info(request)

	if newTeamName != "":
		p = Player.objects.get(id=request.user.id)
		p.name = newTeamName
		p.save()
		error = 0
		msg = "Successfully updated team name"
	else:
		error = 1
		msg = "New Team Name must not be empty"

        data = { "error" : error, "msg" : msg }
        return HttpResponse(json.dumps(data), content_type="application/json")

def updateUsername(request):
	data = json.loads(request.body)
	newUsername = data["new_user_name"]

	if newUsername is not None:
		u = User.objects.get(id=request.user.id)
		u.username = newUsername
		u.save()
		error = 0
		msg = "Successfully updated username"
	else:
                error = 1
                msg = "New Username must not be empty"

        data = { "error" : error, "msg" : msg }
        return HttpResponse(json.dumps(data), content_type="application/json")
