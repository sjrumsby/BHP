from django.shortcuts import render

@login_required
def match_index(request):
        current_time = datetime.now()
        formed_date = "%s-%s-%s" % (current_time.year, str(current_time.month).zfill(2), str(current_time.day).zfill(2))
        pool = Pool.objects.get(pk=1)
        week = pool.current_week

        match = Match.objects.filter(week = week)
        game_ids = []
        match_data = []

        for g in Game.objects.filter(date=formed_date).values_list('home_team', flat="True"):
                game_ids.append(g)
        for g in Game.objects.filter(date=formed_date).values_list('away_team', flat="True"):
                game_ids.append(g)

        if len(match) > 0:
                for m in match:
                        tmp_arr = { 'match' : m, 'home' : { 'score' : 0 }, 'away' : { 'score' : 0 } }
                        tmp_arr['home']['category_points'] = Team_Point.objects.filter(point__week = week, player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                        tmp_arr['away']['category_points'] = Team_Point.objects.filter(point__week = week, player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                        tmp_arr['home']['in_action'] = Activated_Team.objects.filter(player=m.home_player).filter(skater__hockey_team__in=game_ids).count()
                        tmp_arr['away']['in_action'] = Activated_Team.objects.filter(player=m.away_player).filter(skater__hockey_team__in=game_ids).count()

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
                context = {'page_name' : 'Schedule', 'state' : 1, 'matches' : match_data}
        else:
                context = {'page_name' : 'Schedule', 'state' : 0 }
        return render(request, 'hockeypool/match.html', context)

@login_required
def match_detail(request, match_id):
        current_time = datetime.now()
        formed_date = "%s-%s-%s" % (current_time.year, str(current_time.month).zfill(2), str(current_time.day).zfill(2))
        match = Match.objects.select_related().filter(id = match_id)
        game_ids = []
        for g in Game.objects.filter(date=formed_date).values_list('home_team', flat="True"):
                game_ids.append(g)
        for g in Game.objects.filter(date=formed_date).values_list('away_team', flat="True"):
                game_ids.append(g)

        if len(match) > 0:
                match = match[0]
                match_info = []
                week = match.week.number
                m_info = { 'match' : match, 'home' : { 'score' : 0, 'expected' : {'category_points' : {'fantasy_points' : 0, 'goals' : 0, 'assists' : 0, 'plus_minus' : 0, 'offensive_special' : 0, 'true_grit' : 0, 'goalie' : 0, 'shootout' : 0}, 'score' : 0 } }, 'away' : { 'score' : 0, 'expected' : {'category_points' : {'fantasy_points' : 0, 'goals' : 0, 'assists' : 0, 'plus_minus' : 0, 'offensive_special' : 0, 'true_grit' : 0, 'goalie' : 0, 'shootout' : 0}, 'score' : 0 } } }
                m_info['home']['category_points'] = Team_Point.objects.filter(point__week = week, player=match.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                m_info['away']['category_points'] = Team_Point.objects.filter(point__week = week, player=match.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                m_info['home']['in_action'] = Activated_Team.objects.filter(player=match.home_player).filter(skater__hockey_team__in=game_ids).count()
                m_info['away']['in_action'] = Activated_Team.objects.filter(player=match.away_player).filter(skater__hockey_team__in=game_ids).count()

                home_team = Activated_Team.objects.select_related().filter(player = match.home_player)
                home_team_ids = home_team.values_list('skater__hockey_team_id', flat=True)
                away_team = Activated_Team.objects.select_related().filter(player = match.away_player)
                away_team_ids = away_team.values_list('skater__hockey_team_id', flat=True)

                home_daily_action = []
                away_daily_action = []
                for x in Week_Dates.objects.filter(week__number=week):
                        home_daily_action.append(Activated_Team.objects.filter(player=match.home_player).filter(Q(skater__hockey_team__in=Game.objects.filter(date=x.date).values_list('home_team', flat="True")) | (Q(skater__hockey_team__in=Game.objects.filter(date=x.date).values_list('away_team', flat="True")))).count())
                        away_daily_action.append(Activated_Team.objects.filter(player=match.away_player).filter(Q(skater__hockey_team__in=Game.objects.filter(date=x.date).values_list('home_team', flat="True")) | (Q(skater__hockey_team__in=Game.objects.filter(date=x.date).values_list('away_team', flat="True")))).count())

                m_info['home']['daily_action'] = home_daily_action
                m_info['away']['daily_action'] = away_daily_action

                if m_info['home']['category_points']['fantasy_points'] > m_info['away']['category_points']['fantasy_points']:
                        m_info['home']['score'] = m_info['home']['score'] + 2
                elif m_info['home']['category_points']['fantasy_points'] <  m_info['away']['category_points']['fantasy_points']:
                        m_info['away']['score'] = m_info['away']['score'] + 2

                if m_info['home']['category_points']['goals'] > m_info['away']['category_points']['goals']:
                        m_info['home']['score'] = m_info['home']['score'] + 1
                elif m_info['home']['category_points']['goals'] <  m_info['away']['category_points']['goals']:
                        m_info['away']['score'] = m_info['away']['score'] + 1

                if m_info['home']['category_points']['assists'] > m_info['away']['category_points']['assists']:
                        m_info['home']['score'] = m_info['home']['score'] + 1
                elif m_info['home']['category_points']['assists'] <  m_info['away']['category_points']['assists']:
                        m_info['away']['score'] = m_info['away']['score'] + 1

                if m_info['home']['category_points']['plus_minus'] > m_info['away']['category_points']['plus_minus']:
                        m_info['home']['score'] = m_info['home']['score'] + 1
                elif m_info['home']['category_points']['plus_minus'] <  m_info['away']['category_points']['plus_minus']:
                        m_info['away']['score'] = m_info['away']['score'] + 1

                if m_info['home']['category_points']['offensive_special'] > m_info['away']['category_points']['offensive_special']:
                        m_info['home']['score'] = m_info['home']['score'] + 1
                elif m_info['home']['category_points']['offensive_special'] <  m_info['away']['category_points']['offensive_special']:
                        m_info['away']['score'] = m_info['away']['score'] + 1

                if m_info['home']['category_points']['true_grit'] > m_info['away']['category_points']['true_grit']:
                        m_info['home']['score'] = m_info['home']['score'] + 1
                elif m_info['home']['category_points']['true_grit'] <  m_info['away']['category_points']['true_grit']:
                        m_info['away']['score'] = m_info['away']['score'] + 1

                if m_info['home']['category_points']['goalie'] > m_info['away']['category_points']['goalie']:
                        m_info['home']['score'] = m_info['home']['score'] + 1
                elif m_info['home']['category_points']['goalie'] <  m_info['away']['category_points']['goalie']:
                        m_info['away']['score'] = m_info['away']['score'] + 1

                if m_info['home']['score'] == m_info['away']['score']:
                        if m_info['home']['category_points']['shootout'] > m_info['away']['category_points']['shootout']:
                                m_info['home']['score'] = m_info['home']['score'] + 1
                        elif m_info['home']['category_points']['shootout'] <  m_info['away']['category_points']['shootout']:
                                m_info['away']['score'] = m_info['away']['score'] + 1


                home_team_ids = home_team.values_list("skater_id", flat="True")
                m_info['home']['team'] = []

                for h in home_team:
                        tmp_dict = { 'skater' : h.skater }
                        if h.skater.hockey_team.id in game_ids:
                                tmp_dict['active'] = 1
                        else:
                                tmp_dict['active'] = 0
                        tmp_dict['category_points'] = Team_Point.objects.filter(point__week__number = week, point__skater = h.skater).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                        tmp_dict['num_games'] = Game.objects.filter(date__in=Week_Dates.objects.filter(week=match.week).values_list('date', flat="True")).filter(Q(home_team=h.skater.hockey_team)|Q(away_team=h.skater.hockey_team)).count()
                        m_info['home']['team'].append(tmp_dict)

                away_team_ids = away_team.values_list('skater_id', flat="True")
                m_info['away']['team'] = []

                for h in away_team:
                        tmp_dict = { 'skater' : h.skater }
                        if h.skater.hockey_team.id in game_ids:
                                tmp_dict['active'] = 1
                        else:
                                tmp_dict['active'] = 0
                        tmp_dict['category_points'] = Team_Point.objects.filter(point__week__number = week, point__skater = h.skater).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                        tmp_dict['num_games'] = Game.objects.filter(date__in=Week_Dates.objects.filter(week=match.week).values_list('date', flat="True")).filter(Q(home_team=h.skater.hockey_team)|Q(away_team=h.skater.hockey_team)).count()
                        m_info['away']['team'].append(tmp_dict)

                home_expect = Team_Point.objects.filter(player=match.home_player).values('point__week_id').annotate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'), shootout=Sum('point__shootout'))
                away_expect = Team_Point.objects.filter(player=match.away_player).values('point__week_id').annotate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'), shootout=Sum('point__shootout'))

                pool = Pool.objects.get(pk=1)
                week = pool.current_week.number
                start_week = max(0, week-3)
                end_week = min(week, match.week.number)
                week_length = end_week - start_week
                nums = range(0, end_week)

                for i in nums[start_week-1:end_week-1]:
                        if i < len(home_expect):
                                m_info['home']['expected']['category_points']['fantasy_points'] += home_expect[i]['fantasy_points']
                                m_info['home']['expected']['category_points']['goals'] += home_expect[i]['goals']
                                m_info['home']['expected']['category_points']['assists'] += home_expect[i]['assists']
                                m_info['home']['expected']['category_points']['plus_minus'] += home_expect[i]['plus_minus']
                                m_info['home']['expected']['category_points']['offensive_special'] += home_expect[i]['offensive_special']
                                m_info['home']['expected']['category_points']['true_grit'] += home_expect[i]['true_grit']
                                m_info['home']['expected']['category_points']['goalie'] += home_expect[i]['goalie']
                                m_info['home']['expected']['category_points']['shootout'] += home_expect[i]['shootout']
                                m_info['away']['expected']['category_points']['fantasy_points'] += away_expect[i]['fantasy_points']
                                m_info['away']['expected']['category_points']['goals'] += away_expect[i]['goals']
                                m_info['away']['expected']['category_points']['assists'] += away_expect[i]['assists']
                                m_info['away']['expected']['category_points']['plus_minus'] += away_expect[i]['plus_minus']
                                m_info['away']['expected']['category_points']['offensive_special'] += away_expect[i]['offensive_special']
                                m_info['away']['expected']['category_points']['true_grit'] += away_expect[i]['true_grit']
                                m_info['away']['expected']['category_points']['goalie'] += away_expect[i]['goalie']
                                m_info['away']['expected']['category_points']['shootout'] += away_expect[i]['shootout']

                m_info['home']['expected']['category_points']['fantasy_points'] /= week_length
                m_info['home']['expected']['category_points']['goals'] /= week_length
                m_info['home']['expected']['category_points']['assists'] /=week_length
                m_info['home']['expected']['category_points']['plus_minus'] /= week_length
                m_info['home']['expected']['category_points']['offensive_special'] /= week_length
                m_info['home']['expected']['category_points']['true_grit'] /= week_length
                m_info['home']['expected']['category_points']['goalie'] /= week_length
                m_info['home']['expected']['category_points']['shootout'] /= week_length
                m_info['away']['expected']['category_points']['fantasy_points'] /= week_length
                m_info['away']['expected']['category_points']['goals'] /= week_length
                m_info['away']['expected']['category_points']['assists'] /= week_length
                m_info['away']['expected']['category_points']['plus_minus'] /= week_length
                m_info['away']['expected']['category_points']['offensive_special'] /= week_length
                m_info['away']['expected']['category_points']['true_grit'] /= week_length
                m_info['away']['expected']['category_points']['goalie'] /= week_length
                m_info['away']['expected']['category_points']['shootout'] /= week_length

                if m_info['home']['expected']['category_points']['fantasy_points'] > m_info['away']['expected']['category_points']['fantasy_points']:
                        m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 2
                elif m_info['home']['expected']['category_points']['fantasy_points'] <  m_info['away']['expected']['category_points']['fantasy_points']:
                        m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 2

                if m_info['home']['expected']['category_points']['goals'] > m_info['away']['expected']['category_points']['goals']:
                        m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 1
                elif m_info['home']['expected']['category_points']['goals'] <  m_info['away']['expected']['category_points']['goals']:
                        m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 1

                if m_info['home']['expected']['category_points']['assists'] > m_info['away']['expected']['category_points']['assists']:
                        m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 1
                elif m_info['home']['expected']['category_points']['assists'] <  m_info['away']['expected']['category_points']['assists']:
                        m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 1

                if m_info['home']['expected']['category_points']['plus_minus'] > m_info['away']['expected']['category_points']['plus_minus']:
                        m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 1
                elif m_info['home']['expected']['category_points']['plus_minus'] <  m_info['away']['expected']['category_points']['plus_minus']:
                        m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 1

                if m_info['home']['expected']['category_points']['offensive_special'] > m_info['away']['expected']['category_points']['offensive_special']:
                        m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 1
                elif m_info['home']['expected']['category_points']['offensive_special'] <  m_info['away']['expected']['category_points']['offensive_special']:
                        m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 1

                if m_info['home']['expected']['category_points']['true_grit'] > m_info['away']['expected']['category_points']['true_grit']:
                        m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 1
                elif m_info['home']['expected']['category_points']['true_grit'] <  m_info['away']['expected']['category_points']['true_grit']:
                        m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 1

                if m_info['home']['expected']['category_points']['goalie'] > m_info['away']['expected']['category_points']['goalie']:
                        m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 1
                elif m_info['home']['expected']['category_points']['goalie'] <  m_info['away']['expected']['category_points']['goalie']:
                        m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 1

                if m_info['home']['expected']['score'] == m_info['away']['expected']['score']:
                        if m_info['home']['expected']['category_points']['shootout'] > m_info['away']['expected']['category_points']['shootout']:
                                m_info['home']['expected']['score'] = m_info['home']['expected']['score'] + 1
                        elif m_info['home']['expected']['category_points']['shootout'] <  m_info['away']['expected']['category_points']['shootout']:
                                m_info['away']['expected']['score'] = m_info['away']['expected']['score'] + 1



        context = {'page_name' : 'Match: %s' % match_id, 'match' : m_info }
        return render(request, 'hockeypool/match_detail.html', context)

@login_required
def match_week(request, match_week):
        week = match_week
        current_time = datetime.now()
        formed_date = "%s-%s-%s" % (current_time.year, str(current_time.month).zfill(2), str(current_time.day).zfill(2))

        match = Match.objects.select_related().filter(week__number = week)
        game_ids = []
        match_data = []

        for g in Game.objects.filter(date=formed_date).values_list('home_team', flat="True"):
                game_ids.append(g)
        for g in Game.objects.filter(date=formed_date).values_list('away_team', flat="True"):
                game_ids.append(g)

        if len(match) > 0:
                for m in match:
                        tmp_arr = { 'match' : m, 'home' : { 'score' : 0 }, 'away' : { 'score' : 0 } }
                        tmp_arr['home']['category_points'] = Team_Point.objects.filter(point__week = week, player=m.home_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                        tmp_arr['away']['category_points'] = Team_Point.objects.filter(point__week = week, player=m.away_player).aggregate(fantasy_points=Sum('point__fantasy_points'), goals=Sum('point__goals'), assists=Sum('point__assists'), shootout=Sum('point__shootout'), plus_minus=Sum('point__plus_minus'), offensive_special=Sum('point__offensive_special'), true_grit=Sum('point__true_grit_special'), goalie=Sum('point__goalie'))
                        tmp_arr['home']['in_action'] = Activated_Team.objects.filter(player=m.home_player).filter(skater__hockey_team__in=game_ids).count()
                        tmp_arr['away']['in_action'] = Activated_Team.objects.filter(player=m.away_player).filter(skater__hockey_team__in=game_ids).count()

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
                context = {'page_name' : 'Schedule', 'state' : 1, 'matches' : match_data}
        else:
                context = {'page_name' : 'Schedule', 'state' : 0 }
        return render(request, 'hockeypool/match_week.html', context)

@login_required
def match_activate(request):
        activations = Activation.objects.filter(player__id = request.user.id)
        team = Team.objects.filter(player__id = request.user.id).order_by("skater__position")
        team_array = []
        pool = Pool.objects.get(pk=1)
        for t in team:
                date = datetime.now()
                formed_date = "%s-%s-%s" % (date.year, str(date.month).zfill(2), str(date.day).zfill(2))
                current_week = pool.current_week
                next_week = current_week.number + 1
                tmp_arr = {'skater' : t}
                check = 0

                for x in activations:
                        if t.skater.id == x.skater.id:
                                check = 1

                tmp_arr['check'] = check
                tmp_arr['category_points'] = Point.objects.filter(skater = t.skater).aggregate(fantasy_points=Sum('fantasy_points'), goals=Sum('goals'), assists=Sum('assists'), shootout=Sum('shootout'), plus_minus=Sum('plus_minus'), offensive_special=Sum('offensive_special'), true_grit=Sum('true_grit_special'), goalie=Sum('goalie'))
                tmp_arr['num_games'] = Game.objects.filter(date__in=Week_Dates.objects.filter(week__number=next_week).values_list('date', flat="True")).filter(Q(home_team=t.skater.hockey_team)|Q(away_team=t.skater.hockey_team)).count()
                team_array.append(tmp_arr)
        context = {'page_name' : 'Activate', 'team' : team_array}
        return render(request, 'hockeypool/match_activate.html', context)

