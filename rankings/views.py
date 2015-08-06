from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from hockeypool.models import *
from rankings.models import *

import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
        pool = Pool.objects.get(pk=1)
        week = pool.current_week
        last_week_number = week.number - 1
        rankings = Power_Rank.objects.select_related().filter(week=last_week_number).order_by("power_rank")
        ranks = []
        for r in rankings:
                tmp_dict = {'name' : r.player.name}
                tmp_dict['ranking'] = r.power_rank
                if r.week == 1:
                        tmp_dict['old_ranking'] = " - "
                        tmp_dict['change'] = " - "
                else:
                        old_rankings = Power_Rank.objects.filter(week=last_week_number-1).filter(player=r.player)
                        tmp_dict['old_ranking'] = old_rankings[0].power_rank
                        tmp_dict['change'] = tmp_dict['old_ranking'] - tmp_dict['ranking']
                tmp_dict['comment'] = r.comment
                ranks.append(tmp_dict)

        context = {'page_name' : 'Rankings', 'ranks' : ranks}
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
