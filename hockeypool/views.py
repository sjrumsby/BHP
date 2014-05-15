from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Q

from hockeypool.models import *
from draft.models import *
from match.models import *
from trades.models import *
from waivers.models import *

import logging
logger = logging.getLogger(__name__)

def standings_sort(data):
        return sorted(data, key = lambda x: (x['wins'], x['categories'], x['points']['fantasy_points']), reverse=True)

def index(request):
        posts = Post.objects.all().order_by("id")
        posts = posts.reverse()[:5]
	mainFrame = { 'posts' : posts }
	sideFrame = {}
        context = {'page_name' : 'Home', 'mainFrame' : mainFrame, 'sideFrame' : sideFrame}
        return render(request, 'hockeypool/index.html', context)

def freeagents_index(request):
        position = 'F'
        sortby = "goals"
        sortnumber = "50"
        only_freeagents = "0"
        view_type = "0"
        weeks = "0"

        if request.method == 'POST':
                position = request.POST.get('position')
                sortby = request.POST.get('sortby')
                sortnumber = request.POST.get('resultnumber')
                only_freeagents = request.POST.get('only_freeagents')
                weeks = request.POST.get('weeks')
                view_type = request.POST.get('view_type')

        if position == 'F':
                if Team.objects.all().count() == 0:
                        s = Skater.objects.select_related().exclude(position = "G").exclude(id__in = Draft_Pick.objects.filter(pick__isnull=False).values_list('pick_id', flat=True)).order_by("-%s" % sortby)
                else:
                        if only_freeagents == "0":
                                s = Skater.objects.select_related().exclude(position = "G").exclude(id__in = Team.objects.all().values_list('skater_id', flat=True)).order_by("-%s" % sortby)
                        else:
                                s = Skater.objects.select_related().exclude(position = "G").order_by("-%s" % sortby)
        else:
                if Team.objects.all().count() == 0:
                        s = Skater.objects.select_related().filter(position=position).exclude(id__in = Draft_Pick.objects.filter(pick_isnull=False).values_list('skater_id', flat=True)).order_by("-%s" % sortby)
                else:
                        if only_freeagents == "0":
                                s = Skater.objects.select_related().filter(position=position).exclude(id__in = Team.objects.all().values_list('skater_id', flat=True)).order_by("-%s" % sortby)
                        else:
                                s = Skater.objects.select_related().filter(position=position).order_by("-%s" % sortby)
        if sortnumber == "5":
                s = s[:5]
        elif sortnumber == "10":
                s = s[:10]
        elif sortnumber == "25":
                s = s[:25]
        elif sortnumber == "50":
                s = s[:50]
        elif sortnumber == "100":
                s = s[:100]
        elif sortnumber == "250":
                s = s[:250]

        if weeks != "0":
                pool = Pool.objects.get(pk=1)
                current_week = pool.current_week.id
                free_agents = []
                for x in s:
                        tmp_dict = {'skater' : x}
                        tmp_dict['cat_points'] = Point.objects.filter(week__id__gte=current_week-int(weeks)).filter(skater=x).aggregate(fantasy_points=Sum('fantasy_points'), goals=Sum('goals'), assists=Sum('assists'), shootout=Sum('shootout'), plus_minus=Sum('plus_minus'), offensive_special=Sum('offensive_special'), true_grit=Sum('true_grit_special'), goalie=Sum('goalie'))
                        free_agents.append(tmp_dict)
                s = free_agents

        context = {'page_name' : 'Free Agents', 'free_agents' : s, 'position' : position, 'sortby' : sortby, 'sortnumber' : sortnumber, 'only_freeagents' : only_freeagents, 'view_type' : view_type, 'weeks' : weeks}
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
        if request.method == "POST":
                new_name = request.POST.get("change_team_name")
                old_pass = request.POST.get("old_pass")
                new_pass1 = request.POST.get("password1")
                new_pass2 = request.POST.get("password2")
                if new_name != None:
                        if Player.objects.filter(id=user.id).exists():
                                p = Player.objects.get(id=user.id)
                                p.name = new_name
                                p.save()
                        else:
                                p = Player(id=user.id, name=new_name)
                                p.save()
                if new_pass1 != "" and old_pass != "" and new_pass1 == new_pass2:
                        logger.info(old_pass)
                        logger.info("Attempting password reset for user: %s" % request.user)
                        if check_password(old_pass, user.password):
                                hash_pass = make_password(new_pass1)
                                user.password = hash_pass
                                user.save()
                        else:
                                logger.info("Failed: old password does not match new password")
                                logger.info(make_password(old_pass))
                                logger.info(user.password)

        if Player.objects.filter(name=request.user.username).exists():
                p = Player.objects.get(id=user.id)
                team_name = p.get_name()
        else:
                team_name = ""
        context = {'page_name' : 'Profile', 'team_name' : team_name}
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

def standings_index(request):
        players = Player.objects.all()
        standings_data = []
        pool = Pool.objects.get(pk=1)
        current_week = pool.current_week
        for p in players:
                player_data = {'name' : p.name, 'conference' : p.conference}
                player_data['wins'] = Match.objects.filter(winner_player = p).count()
                player_data['loss'] = pool.current_week.number - player_data['wins']
                away_cats = Match.objects.filter(away_player=p).aggregate(Sum('away_cat'))
                home_cats = Match.objects.filter(home_player=p).aggregate(Sum('home_cat'))
                player_data['categories'] = away_cats['away_cat__sum'] + home_cats['home_cat__sum']
                streak_data = Match.objects.filter(winner_player__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('-week')
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

                player_data['points'] = Team_Point.objects.filter(player=p).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                standings_data.append(player_data)
        s_data = standings_sort(standings_data)
        context = {'page_name' : 'Standings', 'p_data' : s_data}
        return render(request, 'hockeypool/standings_index.html', context)

@login_required
def standings_west(request):
        players = Player.objects.filter(conference='West')
        standings_data = []
        pool = Pool.objects.get(pk=1)
        for p in players:
                player_data = {'name' : p.name, 'conference' : p.conference}
                player_data['wins'] = Match.objects.filter(winner_player = p).count()
                player_data['loss'] = pool.current_week.number - player_data['wins']
                away_cats = Match.objects.filter(away_player=p).aggregate(Sum('away_cat'))
                home_cats = Match.objects.filter(home_player=p).aggregate(Sum('home_cat'))
                player_data['categories'] = away_cats['away_cat__sum'] + home_cats['home_cat__sum']
                streak_data = Match.objects.filter(winner_player__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('-week')
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

                player_data['points'] = Team_Point.objects.filter(player=p).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                standings_data.append(player_data)
        s_data = standings_sort(standings_data)
        context = {'page_name' : 'Standings', 'p_data' : s_data}
        return render(request, 'hockeypool/standings_west.html', context)

@login_required
def standings_east(request):
        players = Player.objects.filter(conference='East')
        standings_data = []
        pool = Pool.objects.get(pk=1)
        for p in players:
                player_data = {'name' : p.name, 'conference' : p.conference}
                player_data['wins'] = Match.objects.filter(winner_player = p).count()
                player_data['loss'] = pool.current_week.number - player_data['wins']
                away_cats = Match.objects.filter(away_player=p).aggregate(Sum('away_cat'))
                home_cats = Match.objects.filter(home_player=p).aggregate(Sum('home_cat'))
                player_data['categories'] = away_cats['away_cat__sum'] + home_cats['home_cat__sum']
                streak_data = Match.objects.filter(winner_player__isnull=False).filter(Q(home_player=p)|Q(away_player=p)).order_by('-week')
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

                player_data['points'] = Team_Point.objects.filter(player=p).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                standings_data.append(player_data)
        s_data = standings_sort(standings_data)
        context = {'page_name' : 'Standings', 'p_data' : s_data}

        return render(request, 'hockeypool/standings_east.html', context)

@login_required
def team_index(request):
        context = {'page_name' : 'Team'}
        return render(request, 'hockeypool/team_index.html', context)

@login_required
def team_detail(request, team_id):
        team = Team.objects.filter(player_id=team_id).order_by("skater__position")
        player = Player.objects.filter(id=team_id)[0]
        team_data = []
        for t in team:
                skater_data = {'skater' : t.skater}
                skater_data['category_points'] = Point.objects.filter(skater = t.skater).aggregate(fantasy_points=Sum('fantasy_points'), goals=Sum('goals'), assists=Sum('assists'), shootout=Sum('shootout'), plus_minus=Sum('plus_minus'), offensive_special=Sum('offensive_special'), true_grit=Sum('true_grit_special'), goalie=Sum('goalie'))
                team_data.append(skater_data)

        context = {'page_name' : 'Team: %s' % player.name, 'team' : team_data}
        return render(request, 'hockeypool/team_detail.html', context)

