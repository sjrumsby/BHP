drop materialized view hockey_pool.mv_season_points;
create materialized view hockey_pool.mv_season_points
tablespace apex
refresh force on demand
as
select p.point_skater_id skater_id,
       s.name name,
       s.skater_hockey_team_id hockey_team_id,
       substr(g.nhl_game_id, 0, 4) season,
       sum(p.goals) goals,
       sum(p.assists) assists,
       sum(p.plus_minus) plus_minus,
       sum(p.shg) shg,
       sum(p.sha) sha,
       sum(p.gwa) gwa,
       sum(p.ena) ena,
       sum(p.ppg) ppg,
       sum(p.ppa) ppa,
       sum(p.gwg) gwg,
       sum(p.psg) psg,
       sum(p.eng) eng,
       sum(p.pims) pims,
       sum(p.pims_drawn) pims_drawn,
       sum(p.hits) hits,
       sum(p.shots) shots,
       sum(p.blocked_shots) blocked_shots,
       sum(p.misses) misses,
       sum(p.blocks) blocks,
       sum(p.fights) fights,
       sum(p.giveaways) giveaways,
       sum(p.takeaways) takeaways,
       sum(p.faceoff_wins) fow,
       sum(p.faceoff_losses) fol,
       floor(mod((sum(60 * cast(regexp_substr(p.toi, '[^:]+') as number)) +
                 sum(cast(ltrim(regexp_substr(p.toi, ':[0-9]+'), ':') as
                           number))) / 3600,
                 60)) || ':' ||
       lpad(floor(mod((sum(60 *
                           cast(regexp_substr(p.toi, '[^:]+') as number)) +
                      sum(cast(ltrim(regexp_substr(p.toi, ':[0-9]+'), ':') as
                                number))) / 60,
                      60)),
            2,
            '0') || ':' ||
       lpad(mod((sum(60 * cast(regexp_substr(p.toi, '[^:]+') as number)) +
                sum(cast(ltrim(regexp_substr(p.toi, ':[0-9]+'), ':') as
                          number))),
                60),
            2,
            '0') toi,
       sum(p.shootout_goals) sog,
       sum(p.shootout_misses) som,
       sum(p.wins) wins,
       sum(p.ot_losses) otl,
       sum(p.saves) saves,
       sum(p.shutouts) shutouts,
       sum(p.penshot_saves) ps_saves,
       sum(p.penshot_ga) ps_ga,
       sum(p.shootout_saves) so_saves,
       sum(p.shootout_ga) so_ga,
       sum(p.ga) ga,
       sum(p.first_stars) fs,
       sum(p.second_stars) ss,
       sum(p.third_stars) ts
  from hockey_pool.points p, hockey_pool.nhl_game g, hockey_pool.skaters s
 where p.point_game_id = g.game_id
   and p.point_skater_id = s.skater_id
 group by p.point_skater_id,
          substr(g.nhl_game_id, 0, 4),
          s.name,
          s.skater_hockey_team_id;

