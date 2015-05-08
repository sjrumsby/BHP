spool bhp_packages_install.log

create or replace package hockey_pool.pkg_pool is

procedure insert_skater(p_skater_id number,
                        p_skater_name varchar2,
                        p_skater_team number);

procedure insert_nhl_game(p_game_date date,
                          p_home_team number,
                          p_away_team number,
                          p_nhl_game_id number);

procedure insert_point(p_season_id number,
                       p_game_id number,
                       p_year_id number,
                       p_skater_id number,
                       p_goals number,
                       p_assists number,
                       p_plus_minus number,
                       p_shg number,
                       p_sha number,
                       p_gwa number,
                       p_ena number,
                       p_ppg number,
                       p_ppa number,
                       p_gwg number,
                       p_psg number,
                       p_eng number,
                       p_pims number,
                       p_pims_drawn number,
                       p_hits number,
                       p_shots number,
                       p_blocked_shots number,
                       p_misses number,
                       p_blocks number,
                       p_fights number,
                       p_giveaways number,
                       p_takeaways number,
                       p_faceoff_wins number,
                       p_faceoff_losses number,
                       p_toi varchar2,
                       p_shootout_goals number,
                       p_shootout_misses number,
                       p_wins number,
                       p_ot_losses number,
                       p_saves number,
                       p_shutouts number,
                       p_penshot_saves number,
                       p_penshot_ga number,
                       p_shootout_saves number,
                       p_shootout_ga number,
                       p_ga number,
                       p_first_stars number,
                       p_second_stars number,
                       p_third_stars number);
end pkg_pool;
/

create or replace package body hockey_pool.pkg_pool is
  procedure insert_skater(p_skater_id number,
                          p_skater_name varchar2,
                          p_skater_team number)
  as
    l_count number;
  begin
    select count(*)
      into l_count
      from hockey_pool.skaters s
     where s.skater_id = p_skater_id;

  if l_count = 0 then
    insert into hockey_pool.skaters (skater_id, name, skater_hockey_team_id)
    values (p_skater_id, p_skater_name, p_skater_team);
  end if;
end;

  procedure insert_nhl_game(p_game_date date,
                            p_home_team number,
                            p_away_team number,
                            p_nhl_game_id number)
  as
    l_count number;
  begin
    select count(*)
      into l_count
      from hockey_pool.nhl_game n
     where n.nhl_game_id = p_nhl_game_id;

    if l_count = 0 then
      insert into hockey_pool.nhl_game (game_date, home_team_id, away_team_id, nhl_game_id) 
      values (p_game_date, p_home_team, p_away_team, p_nhl_game_id);
    end if;
  end;

  procedure insert_point(p_season_id number,
                         p_game_id number,
                         p_year_id number,
                         p_skater_id number,
                         p_goals number,
                         p_assists number,
                         p_plus_minus number,
                         p_shg number,
                         p_sha number,
                         p_gwa number,
                         p_ena number,
                         p_ppg number,
                         p_ppa number,
                         p_gwg number,
                         p_psg number,
                         p_eng number,
                         p_pims number,
                         p_pims_drawn number,
                         p_hits number,
                         p_shots number,
                         p_blocked_shots number,
                         p_misses number,
                         p_blocks number,
                         p_fights number,
                         p_giveaways number,
                         p_takeaways number,
                         p_faceoff_wins number,
                         p_faceoff_losses number,
                         p_toi varchar2,
                         p_shootout_goals number,
                         p_shootout_misses number,
                         p_wins number,
                         p_ot_losses number,
                         p_saves number,
                         p_shutouts number,
                         p_penshot_saves number,
                         p_penshot_ga number,
                         p_shootout_saves number,
                         p_shootout_ga number,
                         p_ga number,
                         p_first_stars number,
                         p_second_stars number,
                         p_third_stars number)
  as
    l_count number;
    l_game_id number;
    begin
      select game_id
        into l_game_id
        from hockey_pool.nhl_game n
       where n.nhl_game_id = p_year_id || LPAD(p_season_id,2,'0') || LPAD(p_game_id,4,'0');
        
      select count(*)
        into l_count
        from hockey_pool.points p
       where p.point_skater_id = p_skater_id
         and p.point_game_id = l_game_id;

      if l_count = 0 then
        insert into hockey_pool.points p
          (point_skater_id,
           point_game_id,
           goals,
           assists,
           plus_minus,
           shg,
           sha,
           gwa,
           ena,
           ppg,
           ppa,
           gwg,
           psg,
           eng,
           pims,
           pims_drawn,
           hits,
           shots,
           blocked_shots,
           misses,
           blocks,
           fights,
           giveaways,
           takeaways,
           faceoff_wins,
           faceoff_losses,
           toi,
           shootout_goals,
           shootout_misses,
           wins,
           ot_losses,
           saves,
           shutouts,
           penshot_saves,
           penshot_ga,
           shootout_saves,
           shootout_ga,
           ga,
           first_stars,
           second_stars,
           third_stars)
        values
          (p_skater_id,
           l_game_id,
           p_goals,
           p_assists,
           p_plus_minus,
           p_shg,
           p_sha,
           p_gwa,
           p_ena,
           p_ppg,
           p_ppa,
           p_gwg,
           p_psg,
           p_eng,
           p_pims,
           p_pims_drawn,
           p_hits,
           p_shots,
           p_blocked_shots,
           p_misses,
           p_blocks,
           p_fights,
           p_giveaways,
           p_takeaways,
           p_faceoff_wins,
           p_faceoff_losses,
           p_toi,
           p_shootout_goals,
           p_shootout_misses,
           p_wins,
           p_ot_losses,
           p_saves,
           p_shutouts,
           p_penshot_saves,
           p_penshot_ga,
           p_shootout_saves,
           p_shootout_ga,
           p_ga,
           p_first_stars,
           p_second_stars,
           p_third_stars);
      else
        update hockey_pool.points p
           set p.goals = p_goals,
               p.assists=p_assists,
               p.plus_minus=p_plus_minus,
               p.shg=p_shg,
               p.sha=p_sha,
               p.gwa=p_gwa,
               p.ena=p_ena,
               p.ppg=p_ppg,
               p.ppa=p_ppa,
               p.gwg=p_gwg,
               p.psg=p_psg,
               p.eng=p_eng,
               p.pims=p_pims,
               p.pims_drawn=p_pims_drawn,
               p.hits=p_hits,
               p.shots=p_shots,
               p.blocked_shots=p_blocked_shots,
               p.misses=p_misses,
               p.blocks=p_blocks,
               p.fights=p_fights,
               p.giveaways=p_giveaways,
               p.takeaways=p_takeaways,
               p.faceoff_wins=p_faceoff_wins,
               p.faceoff_losses=p_faceoff_losses,
               p.toi=p_toi,
               p.shootout_goals=p_shootout_goals,
               p.shootout_misses=p_shootout_misses,
               p.wins=p_wins,
               p.ot_losses=p_ot_losses,
               p.saves=p_saves,
               p.shutouts=p_shutouts,
               p.penshot_saves=p_penshot_saves,
               p.penshot_ga=p_penshot_ga,
               p.shootout_saves=p_shootout_saves,
               p.shootout_ga=p_shootout_ga,
               p.ga=p_ga,
               p.first_stars=p_first_stars,
               p.second_stars=p_second_stars,
               p.third_stars=p_third_stars
         where p.point_skater_id = p_skater_id
           and p.point_game_id = l_game_id;
      end if;
    end;
end pkg_pool; 
/

spool off;

