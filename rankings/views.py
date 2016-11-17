from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from hockeypool.models import *
from rankings.models import *
from match.models import *
from django.db.models import Sum, Q
import logging
logger = logging.getLogger(__name__)

def standings_sort(data):
        return sorted(data, key = lambda x: (x['wins'], x['cats'], x['fpfpg']), reverse=True)

@login_required
def index(request):
        pool = Pool.objects.get(pk=1)
        week = pool.current_week
        last_week_number = week.number - 1
        rankings = Power_Rank.objects.select_related().filter(week=last_week_number).order_by("power_rank")
        ranks = []
        for r in rankings:
		logger.info(r)
                tmp_dict = {'name' : r.player.name}
                tmp_dict['ranking'] = r.power_rank
                if r.week == 1:
                        tmp_dict['old_ranking'] = " - "
                        tmp_dict['change'] = " - "
                else:
                        old_rankings = Power_Rank.objects.filter(week=last_week_number-1).filter(player=r.player)
			logger.info("%s-%s" % (last_week_number-1,r.player))
                        tmp_dict['old_ranking'] = old_rankings[0].power_rank
                        tmp_dict['change'] = tmp_dict['old_ranking'] - tmp_dict['ranking']
                tmp_dict['comment'] = r.comment
                ranks.append(tmp_dict)

	players = Player.objects.all()
	player_arr = []
	for p in players:
		tmp_dct = {}
		if week.number == 2:
			weeks = [week.id - 1]
		elif week.number == 3:
			weeks = [week.id -2, week.id - 2]
		elif week.number >= 4:
			weeks = [week.id -2, week.id - 2, week.id - 3]
		else:
			weeks = ()
		wins = Match.objects.filter(week_id__in=weeks).filter(winner_player=p).count()
		home_cats = Match.objects.filter(week_id__in=weeks).filter(home_player=p).aggregate(cats=Sum('home_cat'))
		away_cats = Match.objects.filter(week_id__in=weeks).filter(away_player=p).aggregate(cats=Sum('away_cat'))
		if home_cats['cats'] == None:
			home_cats['cats'] = 0
		if away_cats['cats'] == None:
			away_cats['cats'] = 0
		tmp_dct['cats'] = home_cats['cats'] + away_cats['cats']
		fpfg = Team_Point.objects.filter(player=p).filter(point__date__in=Week_Date.objects.filter(week_id__in=weeks).values_list('date', flat=True)).aggregate(fantasy_points=Sum('point__fantasy_points'))
		tmp_dct['player_name'] = p.name
		tmp_dct['wins'] = wins
		tmp_dct['fpfpg'] = int(fpfg['fantasy_points']/len(weeks))
		tmp_dct['fpapg'] = 0

                for m in Match.objects.filter(week_id__in=weeks).filter(Q(home_player=p)|Q(away_player=p)).order_by('week'):
                        if m.home_player == p:
                                data = Team_Point.objects.filter(point__game__date__in = Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'))
                        else:
                                data = Team_Point.objects.filter(point__game__date__in=Week_Date.objects.filter(week=m.week).values_list('date', flat=True), player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'))

			tmp_dct['fpapg'] += data["fantasy_points"]
		tmp_dct['fpapg'] = int(tmp_dct['fpapg']/len(weeks))
		player_arr.append(tmp_dct)
	player_arr = standings_sort(player_arr)
        context = {'page_name' : 'Rankings', 'ranks' : ranks, "week" : week.number, "players" : player_arr}
        return render(request, 'rankings/index.html', context)

@login_required
def rankings_week(request, rankings_week):
        week = Week.objects.filter(number=rankings_week)
        week = week[0]
        rankings = Power_Rank.objects.select_related().filter(week=week.number).order_by("power_rank")
        ranks = []
        for r in rankings:
                tmp_dict = {'name' : r.player.name}
                tmp_dict['ranking'] = r.power_rank
                if r.week == 1:
                        tmp_dict['old_ranking'] = " - "
                        tmp_dict['change'] = " - "
                else:
                        old_rankings = Power_Rank.objects.filter(week=week.number-1).filter(player=r.player)
                        tmp_dict['old_ranking'] = old_rankings[0].power_rank
                        tmp_dict['change'] = tmp_dict['old_ranking'] - tmp_dict['ranking']
                tmp_dict['comment'] = r.comment
                ranks.append(tmp_dict)

        logger.info(ranks)

        context = {'page_name' : 'Rankings', 'ranks' : ranks}

        return render(request, 'rankings/rankings_week.html', context)
