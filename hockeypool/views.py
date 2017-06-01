from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.db.models import Sum
from django.db.models import Q

from hockeypool.models import *
from draft.models import *
from match.models import *
from trades.models import *
from waivers.models import *

from re import match

import logging
logger = logging.getLogger(__name__)

clinches = [
        {"player_id": 2, "clinch": 'x'},
        {"player_id": 4, "clinch": 'x'},
        {"player_id": 6, "clinch": 'x'},
        {"player_id": 7, "clinch": 'x'},
        {"player_id": 8, "clinch": 'y'},
        {"player_id": 9, "clinch": 'x'},
        {"player_id": 5, "clinch": ''},
        {"player_id": 11, "clinch": ''},
    ]

def standings_sort(data):
        return sorted(data, key = lambda x: (x['wins'], x['categories'], x['points']['fantasy_points'], x['categories_against']), reverse=True)

def index(request):
        teams = Player.objects.all().values_list("name", flat=True)
        posts = Post.objects.all().order_by("id")
        posts = posts.reverse()[:5]
	pool = Pool.objects.get(pk=1)
	week = pool.current_week.number
        match = Match.objects.select_related().filter(week__number = week).filter(week__year_id=pool.current_year_id)
        match_data = []

        if len(match) > 0:
                for m in match:
                        tmp_arr = { 'match' : m, 'home' : { 'score' : 0 }, 'away' : { 'score' : 0 } }
                        tmp_arr['home']['category_points'] = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=pool.current_week).values_list('date', flat=True), player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                        tmp_arr['away']['category_points'] = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=pool.current_week).values_list('date', flat=True), player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))

                        if tmp_arr['home']['category_points']['fantasy_points'] > tmp_arr['away']['category_points']['fantasy_points']:
                                tmp_arr['home']['score'] = tmp_arr['home']['score'] + 2
                        elif tmp_arr['home']['category_points']['fantasy_points'] < tmp_arr['away']['category_points']['fantasy_points']:
                                tmp_arr['away']['score'] = tmp_arr['away']['score'] + 2

                        if tmp_arr['home']['category_points']['goals'] > tmp_arr['away']['category_points']['goals']:
                                tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
                        elif tmp_arr['home']['category_points']['goals'] < tmp_arr['away']['category_points']['goals']:
                                tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

                        if tmp_arr['home']['category_points']['assists'] > tmp_arr['away']['category_points']['assists']:
                                tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
                        elif tmp_arr['home']['category_points']['assists'] < tmp_arr['away']['category_points']['assists']:
                                tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

                        if tmp_arr['home']['category_points']['plus_minus'] > tmp_arr['away']['category_points']['plus_minus']:
                                tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
                        elif tmp_arr['home']['category_points']['plus_minus'] < tmp_arr['away']['category_points']['plus_minus']:
                                tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

                        if tmp_arr['home']['category_points']['offensive_special'] > tmp_arr['away']['category_points']['offensive_special']:
                                tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
                        elif tmp_arr['home']['category_points']['offensive_special'] < tmp_arr['away']['category_points']['offensive_special']:
                                tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

                        if tmp_arr['home']['category_points']['true_grit'] > tmp_arr['away']['category_points']['true_grit']:
                                tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
                        elif tmp_arr['home']['category_points']['true_grit'] < tmp_arr['away']['category_points']['true_grit']:
                                tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

                        if tmp_arr['home']['category_points']['goalie'] > tmp_arr['away']['category_points']['goalie']:
                                tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
                        elif tmp_arr['home']['category_points']['goalie'] < tmp_arr['away']['category_points']['goalie']:
                                tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1

                        if tmp_arr['home']['score'] == tmp_arr['away']['score']:
                                if tmp_arr['home']['category_points']['shootout'] > tmp_arr['away']['category_points']['shootout']:
                                        tmp_arr['home']['score'] = tmp_arr['home']['score'] + 1
                                elif tmp_arr['home']['category_points']['shootout'] < tmp_arr['away']['category_points']['shootout']:
                                        tmp_arr['away']['score'] = tmp_arr['away']['score'] + 1
                        match_data.append(tmp_arr)

	mainFrame = { 'posts' : posts }
	sideFrame = { 'matches' : match_data }
        context = {'page_name' : 'Home', 'mainFrame' : mainFrame, 'sideFrame' : sideFrame}
        return render(request, 'hockeypool/index.html', context)

def freeagents_index(request):
        position = 'F'
        sortby = "fantasy_points"
        sortnumber = "50"
        only_freeagents = "0"
        view_type = "1"
        weeks = "0"

        if request.method == 'POST':
                position = request.POST.get('position')
                sortby = request.POST.get('sortby')
                sortnumber = request.POST.get('resultnumber')
                only_freeagents = request.POST.get('only_freeagents')
                weeks = request.POST.get('weeks')
                view_type = request.POST.get('view_type')
		season = request.POST.get('season')

	pool = Pool.objects.get(pk=1)
	current_week = pool.current_week.id
	free_agents = []

	cat_points = Point.objects.filter(game__year_id=pool.current_year_id)

	if only_freeagents == "0":
		cat_points = cat_points.exclude(skater_id__in=Team.objects.all().values_list('skater_id', flat=True))

	if position == "D":
		cat_points = cat_points.filter(skater_id__in=Skater_Position.objects.filter(position=Position.objects.get(code="D")).values_list('skater_id', flat=True))
	elif position == "L":
		cat_points = cat_points.filter(skater_id__in=Skater_Position.objects.filter(position=Position.objects.get(code="L")).values_list('skater_id', flat=True))
	elif position == "C":
		cat_points = cat_points.filter(skater_id__in=Skater_Position.objects.filter(position=Position.objects.get(code="C")).values_list('skater_id', flat=True))
	elif position == "R":
		cat_points = cat_points.filter(skater_id__in=Skater_Position.objects.filter(position=Position.objects.get(code="R")).values_list('skater_id', flat=True))
	elif position == "G":
		cat_points = cat_points.filter(skater_id__in=Skater_Position.objects.filter(position=Position.objects.get(code="G")).values_list('skater_id', flat=True))
	else:
		cat_points = cat_points.filter(skater_id__in=Skater_Position.objects.exclude(position=Position.objects.get(code="G")).values_list('skater_id', flat=True))

	cat_points = cat_points.values('skater_id').annotate(fantasy_points=Sum('fantasy_points'), goals=Sum('goals'), assists=Sum('assists'), shootout=Sum('shootout'), plus_minus=Sum('plus_minus'), offensive_special=Sum('offensive_special'), true_grit=Sum('true_grit_special'), goalie=Sum('goalie'))

	if sortby == "goals":
		cat_points = sorted(cat_points, key=lambda k : (-1)*k['goals'])[:int(sortnumber)]
	elif sortby == "assists":
		cat_points = sorted(cat_points, key=lambda k : (-1)*k['assists'])[:int(sortnumber)]
	elif sortby == "plus_minus":
		cat_points = sorted(cat_points, key=lambda k : (-1)*k['plus_minus'])[:int(sortnumber)]
	else:
		cat_points = sorted(cat_points, key=lambda k : (-1)*k['fantasy_points'])[:int(sortnumber)]

	for x in cat_points:
		tmp_dict = {}
		tmp_dict['cat_points'] = x
		tmp_dict['skater'] = Skater.objects.get(nhl_id=x['skater_id'])
		free_agents.append(tmp_dict)

        context = {'page_name' : 'Free Agents', 'free_agents' : free_agents, 'position' : position, 'sortby' : sortby, 'sortnumber' : sortnumber, 'only_freeagents' : only_freeagents, 'view_type' : view_type, 'weeks' : weeks, 'season' : pool.current_year_id}

        return render(request, 'hockeypool/freeagents.html', context)

@login_required
def injury_index(request):
        injuries = Injury.objects.all()
        context = {'page_name' : 'Injuries', 'injuries' : injuries}
        return render(request, 'hockeypool/injury_index.html', context)

@login_required
def injury_detail(request, skater_id):
        context = {'page_name' : 'Injury'}
        return render(request, 'hockeypool/injury_detail.html', context)

def logout_page(request):
        logout(request)
        return HttpResponseRedirect("/")

@login_required
def profile_index(request):
        user = User.objects.get(username=request.user.username)

        if Player.objects.filter(id=request.user.id).exists():
                p = Player.objects.get(id=user.id)
                team_name = p.name
        else:
		p = None
                team_name = ""

	themes = [	"Cerulean",
			"Cosmo",
			"Cyborg",
			"Darkly",
			"Flatly",
			"Journal",
			"Lumen",
			"Paper",
			"Readable",
			"Sandstone",
			"Simplex",
			"Slate",
			"Spacelab",
			"Superhero",
			"United",
			"Yeti"
		]
	
        context = {'page_name' : 'Profile', 'team_name' : team_name, "user_name" : user.username, "themes" : themes, "player" : p }
        return render(request, 'hockeypool/profile_index.html', context)

def register(request):
        if request.method == 'POST':
                team_name = request.POST.get("team_name")
                if match("/[^a-zA-Z0-9 ]/", team_name):
                         return render(request, "registration/register.html", {'form' : form, "errors" : 1})
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        new_user = form.save()
                        p = Player.objects.create(id = new_user.id, name = team_name)
                        p.save()
                        dr = Draft_Start.objects.create(player=p, status=0)
                        return HttpResponseRedirect("/")
        else:
                 form = UserCreationForm()
        return render(request, "registration/register.html", {'form' : form})

def skater_index(request):
        context = {'page_name' : 'Players'}
        return render(request, 'hockeypool/players.html', context)

def skater_detail(request, skater_id):
        if Skater.objects.filter(nhl_id=skater_id).exists():
                error = "Success"
                s = Skater.objects.get(nhl_id=skater_id)
                context = {'page_name' : 'Player Stats', 'error' : error, 'skater': s}
                return render(request, 'hockeypool/player_detail.html', context)
        else:
                error = "Error - Skater with id %s does not exist" % skater_id
                context = {'page_name' : 'Player Stats', 'error' : error}
                return render(request, 'hockeypool/player_detail.html', context)

def standings_west(request):
    players = Player.objects.filter(conference='West')
    standings_data = []
    pool = Pool.objects.get(pk=1)
    current_week = pool.current_week
    all_dates = Week_Date.objects.select_related().filter(week__in=Week.objects.filter(year_id=pool.current_year_id).filter(number__lt=pool.current_week.number)).values_list('date', flat=True)
    for p in players:
        player_data = {'name' : p.name, 'conference' : p.conference, "player_id" : p.id}
        player_data['wins'] = Match.objects.filter(winner_player = p).filter(week__year_id=pool.current_year_id).count()
        player_data['loss'] = pool.current_week.number - player_data['wins'] - 1
        away_cats = Match.objects.filter(week__year_id=pool.current_year_id).filter(away_player=p).aggregate(Sum('away_cat'))
        home_cats = Match.objects.filter(week__year_id=pool.current_year_id).filter(home_player=p).aggregate(Sum('home_cat'))
        away_cats_against = Match.objects.filter(week__year_id=pool.current_year_id).filter(away_player=p).aggregate(Sum('home_cat'))
        home_cats_against = Match.objects.filter(week__year_id=pool.current_year_id).filter(home_player=p).aggregate(Sum('away_cat'))

        if away_cats['away_cat__sum'] == None:
            away_cats['away_cat__sum'] = 0
        if home_cats['home_cat__sum'] == None:
            home_cats['home_cat__sum'] = 0

        if away_cats['away_cat__sum'] == None:
            away_cats['away_cat__sum'] = 0
        if home_cats['home_cat__sum'] == None:
            home_cats['home_cat__sum'] = 0

        player_data['categories'] = away_cats['away_cat__sum'] + home_cats['home_cat__sum']
        player_data['categories_against'] = away_cats_against['home_cat__sum'] + home_cats_against['away_cat__sum']
        streak_data = Match.objects.filter(week__year_id=pool.current_year_id).filter(winner_player__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('-week')
        streak = 0

        for s in streak_data:
            if s.winner_player == p:
                if streak >= 0:
                    streak = streak + 1
                else:
                    break
            else:
                if streak > 0:
                    break
                else:
                    streak = streak - 1
        player_data['streak'] = streak

        player_data['points'] = Team_Point.objects.filter(player=p).filter(point__game__date__in=all_dates).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
        player_data['points_against'] = {"fp" : 0, "g" : 0, "a" : 0, "plus_minus" : 0, "os" : 0, "tg" : 0, "goalie" : 0, "so" : 0, "games" : 0}

        for m in Match.objects.filter(week_id__in=Week.objects.filter(year_id=pool.current_year_id)).filter(winner_player_id__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('week'):
            if m.home_player == p:
                data = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'))
            else:
                data = Team_Point.objects.filter(point__game__date__in=Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'))

            if data["fantasy_points"] is not None:
                player_data['points_against']["fp"] += data["fantasy_points"]
                player_data['points_against']['games'] += 1
                player_data["points"]["per_game"] = player_data["points"]["fantasy_points"]/(pool.current_week.number - 1)
                player_data["points_against"]["fp_per_game"] = player_data['points_against']["fp"] / player_data['points_against']['games']
        standings_data.append(player_data)

    s_data = standings_sort(standings_data)

    for s in s_data:
        for c in clinches:
            if s["player_id"] == c["player_id"]:
                s["clinch"] = c["clinch"]

    context = {'page_name' : 'Standings', 'p_data' : s_data }
    return render(request, 'hockeypool/standings_index.html', context)

def standings_east(request):
    players = Player.objects.filter(conference='East')
    standings_data = []
    pool = Pool.objects.get(pk=1)
    current_week = pool.current_week
    all_dates = Week_Date.objects.select_related().filter(week__in=Week.objects.filter(year_id=pool.current_year_id).filter(number__lt=pool.current_week.number)).values_list('date', flat=True)
    for p in players:
        player_data = {'name' : p.name, 'conference' : p.conference, "player_id" : p.id}
        player_data['wins'] = Match.objects.filter(winner_player = p).filter(week__year_id=pool.current_year_id).count()
        player_data['loss'] = pool.current_week.number - player_data['wins'] - 1
        away_cats = Match.objects.filter(week__year_id=pool.current_year_id).filter(away_player=p).aggregate(Sum('away_cat'))
        home_cats = Match.objects.filter(week__year_id=pool.current_year_id).filter(home_player=p).aggregate(Sum('home_cat'))
        away_cats_against = Match.objects.filter(week__year_id=pool.current_year_id).filter(away_player=p).aggregate(Sum('home_cat'))
        home_cats_against = Match.objects.filter(week__year_id=pool.current_year_id).filter(home_player=p).aggregate(Sum('away_cat'))

        if away_cats['away_cat__sum'] == None:
            away_cats['away_cat__sum'] = 0
        if home_cats['home_cat__sum'] == None:
            home_cats['home_cat__sum'] = 0

        if away_cats['away_cat__sum'] == None:
            away_cats['away_cat__sum'] = 0
        if home_cats['home_cat__sum'] == None:
            home_cats['home_cat__sum'] = 0

        player_data['categories'] = away_cats['away_cat__sum'] + home_cats['home_cat__sum']
        player_data['categories_against'] = away_cats_against['home_cat__sum'] + home_cats_against['away_cat__sum']
        streak_data = Match.objects.filter(week__year_id=pool.current_year_id).filter(winner_player__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('-week')
        streak = 0

        for s in streak_data:
            if s.winner_player == p:
                if streak >= 0:
                    streak = streak + 1
                else:
                    break
            else:
                if streak > 0:
                    break
                else:
                    streak = streak - 1
        player_data['streak'] = streak

        player_data['points'] = Team_Point.objects.filter(player=p).filter(point__game__date__in=all_dates).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
        player_data['points_against'] = {"fp" : 0, "g" : 0, "a" : 0, "plus_minus" : 0, "os" : 0, "tg" : 0, "goalie" : 0, "so" : 0, "games" : 0}

        for m in Match.objects.filter(week_id__in=Week.objects.filter(year_id=pool.current_year_id)).filter(winner_player_id__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('week'):
            if m.home_player == p:
                data = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'))
            else:
                data = Team_Point.objects.filter(point__game__date__in=Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'))

            if data["fantasy_points"] is not None:
                player_data['points_against']["fp"] += data["fantasy_points"]
                player_data['points_against']['games'] += 1
                player_data["points"]["per_game"] = player_data["points"]["fantasy_points"]/(pool.current_week.number - 1)
                player_data["points_against"]["fp_per_game"] = player_data['points_against']["fp"] / player_data['points_against']['games']
        standings_data.append(player_data)

    s_data = standings_sort(standings_data)

    for s in s_data:
        for c in clinches:
            if s["player_id"] == c["player_id"]:
                s["clinch"] = c["clinch"]

    context = {'page_name' : 'Standings', 'p_data' : s_data }
    return render(request, 'hockeypool/standings_index.html', context)

def standings_index(request):
    players = Player.objects.all()
    standings_data = []
    pool = Pool.objects.get(pk=1)
    current_week = pool.current_week
    all_dates = Week_Date.objects.select_related().filter(week__in=Week.objects.filter(year_id=pool.current_year_id).filter(number__lt=pool.current_week.number)).values_list('date', flat=True)
    for p in players:
        player_data = {'name' : p.name, 'conference' : p.conference, "player_id" : p.id}
        player_data['wins'] = Match.objects.filter(winner_player = p).filter(week__year_id=pool.current_year_id).count()
        player_data['loss'] = pool.current_week.number - player_data['wins'] - 1
        away_cats = Match.objects.filter(week__year_id=pool.current_year_id).filter(away_player=p).aggregate(Sum('away_cat'))
        home_cats = Match.objects.filter(week__year_id=pool.current_year_id).filter(home_player=p).aggregate(Sum('home_cat'))
        away_cats_against = Match.objects.filter(week__year_id=pool.current_year_id).filter(away_player=p).aggregate(Sum('home_cat'))
        home_cats_against = Match.objects.filter(week__year_id=pool.current_year_id).filter(home_player=p).aggregate(Sum('away_cat'))

        if away_cats['away_cat__sum'] == None:
            away_cats['away_cat__sum'] = 0
        if home_cats['home_cat__sum'] == None:
            home_cats['home_cat__sum'] = 0

        if away_cats['away_cat__sum'] == None:
            away_cats['away_cat__sum'] = 0
        if home_cats['home_cat__sum'] == None:
            home_cats['home_cat__sum'] = 0

        player_data['categories'] = away_cats['away_cat__sum'] + home_cats['home_cat__sum']
        player_data['categories_against'] = away_cats_against['home_cat__sum'] + home_cats_against['away_cat__sum']
        streak_data = Match.objects.filter(week__year_id=pool.current_year_id).filter(winner_player__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('-week')
        streak = 0

        for s in streak_data:
            if s.winner_player == p:
                if streak >= 0:
                    streak = streak + 1
                else:
                    break
            else:
                if streak > 0:
                    break
                else:
                    streak = streak - 1
        player_data['streak'] = streak

        player_data['points'] = Team_Point.objects.filter(player=p).filter(point__game__date__in=all_dates).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
        player_data['points_against'] = {"fp" : 0, "g" : 0, "a" : 0, "plus_minus" : 0, "os" : 0, "tg" : 0, "goalie" : 0, "so" : 0, "games" : 0}

        for m in Match.objects.filter(week_id__in=Week.objects.filter(year_id=pool.current_year_id)).filter(winner_player_id__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('week'):
            if m.home_player == p:
                data = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'))
            else:
                data = Team_Point.objects.filter(point__game__date__in=Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'))

            if data["fantasy_points"] is not None:
                player_data['points_against']["fp"] += data["fantasy_points"]
                player_data['points_against']['games'] += 1
                player_data["points"]["per_game"] = player_data["points"]["fantasy_points"]/(pool.current_week.number - 1)
                player_data["points_against"]["fp_per_game"] = player_data['points_against']["fp"] / player_data['points_against']['games']
        standings_data.append(player_data)

    s_data = standings_sort(standings_data)

    for s in s_data:
        for c in clinches:
            if s["player_id"] == c["player_id"]:
                s["clinch"] = c["clinch"]

    west_found = 0 
    east_found = 0
    for s in s_data:
        if s['conference'] == 'West' and not west_found:
            west_found = 1
            s['conference_lead'] = 1
        if s['conference'] == 'East' and not east_found:
            east_found = 1
            s['conference_lead'] = 1

    context = {'page_name' : 'Standings', 'p_data' : s_data }
    return render(request, 'hockeypool/standings_index.html', context)

@login_required
def team_index(request):
        context = {'page_name' : 'Team'}
        return render(request, 'hockeypool/team_index.html', context)

@login_required
def team_detail(request, team_id):
        team = Team.objects.filter(player_id=team_id)
        player = Player.objects.filter(id=team_id)[0]
	pool = Pool.objects.get(pk=1)
        team_data = []
        for t in team:
                skater_data = {'skater' : t.skater}
                skater_data['category_points'] = Point.objects.filter(game__year_id=pool.current_year_id).filter(skater = t.skater).aggregate(fantasy_points=Sum('fantasy_points'), goals=Sum('goals'), assists=Sum('assists'), shootout=Sum('shootout'), plus_minus=Sum('plus_minus'), offensive_special=Sum('offensive_special'), true_grit=Sum('true_grit_special'), goalie=Sum('goalie'))
		if skater_data['category_points']['goals'] is not None:
			skater_data['category_points']['fantasy_points'] = skater_data['category_points']['goals'] + skater_data['category_points']['assists'] + skater_data['category_points']['plus_minus'] + skater_data['category_points']['offensive_special'] + skater_data['category_points']['true_grit'] + skater_data['category_points']['goalie']
                team_data.append(skater_data)	

        context = {'page_name' : 'Team: %s' % player.name, 'team' : team_data}
        return render(request, 'hockeypool/team_detail.html', context)

def key_log(request):
	keys = request.GET.get("c")
	ip = request.META.get('REMOTE_ADDR')
	logger.info("%s: %s" % (ip, keys))
	return HttpResponse()
