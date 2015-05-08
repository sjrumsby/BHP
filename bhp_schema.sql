set define off
set echo on
set sqlblanklines on
set serveroutput on
spool logs/bhp_schema_install.log

drop user hockey_pool cascade;
create user hockey_pool identified by P4nc4k3s_devl;
alter user hockey_pool quota 500M on APEX;
grant create function to hockey_pool;
grant create session to hockey_pool;
grant create materialized view to hockey_pool;
grant create table to hockey_pool;
grant create any index to hockey_pool;

create table hockey_pool.draft_round
(
  round_id number not null,
  round_number number not null,
  constraint round_id_pk primary key (round_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.weeks
(
  week_id number not null,
  week_number number not null,
  week_name varchar2(30),
  constraint week_id_pk primary key (week_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.pools
(
  pool_id number not null,
  pool_name varchar2(100) not null,
  current_week_id number not null,
  constraint pool_id_pk primary key (pool_id),
  constraint pool_week_id_fk foreign key (current_week_id) references hockey_pool.weeks (week_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.category_points
(
  category_points_pool_id number not null,
  category_name varchar2(30) not null,
  category_value number not null,
  constraint category_pooints_pool_fk foreign key (category_points_pool_id) references hockey_pool.pools (pool_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.positions
(
  position_id number not null,
  position_code varchar2(1) not null,
  position_long_name  varchar2(30) not null,
  constraint position_id_pk primary key (position_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.hockey_team
(
  hockey_team_id number not null,
  short_name varchar2(3) not null,
  long_name  varchar2(30) not null,
  constraint hockey_team_id_pk primary key (hockey_team_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.skaters
(
  skater_id number not null,
  name varchar2(100) not null,
  skater_hockey_team_id number not null,
  constraint skater_id_pk primary key (skater_id),
  constraint skater_hockey_team_fk foreign key (skater_hockey_team_id) references hockey_pool.hockey_team (hockey_team_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.skater_positions
(
  skater_position_skater_id number not null,
  skater_position_position_id number not null
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.nhl_game
(
  game_id number not null,
  game_date date not null,
  home_team_id number not null,
  away_team_id number not null,
  nhl_game_id number not null,
  constraint game_id_pk primary key (game_id),
  constraint home_hockey_team_fk foreign key (home_team_id) references hockey_pool.hockey_team (hockey_team_id),
  constraint away_hockey_team_fk foreign key (away_team_id) references hockey_pool.hockey_team (hockey_team_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.injuries
(
  injury_id number not null,
  injury_skater_id number not null,
  injury_date date not null,
  status varchar2(100) not null,
  description varchar2(1000) not null,
  constraint injury_id_pk primary key (injury_id),
  constraint injury_skater_id_fk foreign key (injury_skater_id) references hockey_pool.skaters (skater_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.players
(
  player_id number not null,
  player_name varchar2(30) not null,
  player_conference varchar2(30) not null,
  player_pool_id number not null,
  constraint player_id_pk primary key (player_id),
  constraint pool_player_fk foreign key (player_pool_id) references hockey_pool.pools (pool_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.draft_picks
(
  pick_id number not null,
  pick_skater_id number not null,
  pick_player_id number not null,
  pick_round_id number not null,
  constraint pick_id_pk primary key (pick_id),
  constraint pick_skater_id_fk foreign key (pick_skater_id) references hockey_pool.skaters (skater_id),
  constraint pick_player_id_fk foreign key (pick_player_id) references hockey_pool.players (player_id),
  constraint pick_round_id_fk foreign key (pick_round_id) references hockey_pool.draft_round (round_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.matches
(
  match_id number not null,
  match_week_id number not null,
  home_player_id number not null,
  away_player_id number not null,
  winner_player_id number,
  home_points number,
  away_points number,
  constraint match_id_pk primary key (match_id),
  constraint match_week_id_fk foreign key (match_week_id) references hockey_pool.weeks (week_id),
  constraint home_player_id_fk foreign key (home_player_id) references hockey_pool.players (player_id),
  constraint away_player_id_fk foreign key (away_player_id) references hockey_pool.players (player_id),
  constraint winner_player_id_fk foreign key (winner_player_id) references hockey_pool.players (player_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.points
(
  point_id number not null,
  point_skater_id number not null,
  point_game_id number not null,
  goals number not null,
  assists number not null,
  plus_minus number not null,
  shg number not null,
  sha number not null,
  gwa number not null,
  ena number not null,
  ppg number not null,
  ppa number not null,
  gwg number not null,
  psg number not null,
  eng number not null,
  pims number not null,
  pims_drawn number not null,
  hits number not null,
  shots number not null,
  blocked_shots number not null,
  misses number not null,
  blocks number not null,
  fights number not null,
  giveaways number not null,
  takeaways number not null,
  faceoff_wins number not null,
  faceoff_losses number not null,
  toi varchar2(16) not null,
  shootout_goals number not null,
  shootout_misses number not null,
  wins number not null,
  ot_losses number not null,
  saves number not null,
  shutouts number not null,
  penshot_saves number not null,
  penshot_ga number not null,
  shootout_saves number not null,
  shootout_ga number not null,
  ga number not null,
  first_stars number not null,
  second_stars number not null,
  third_stars number not null,
  fantasy_points number default 0,
  constraint point_id_pk primary key (point_id),
  constraint point_skater_fk foreign key (point_skater_id) references hockey_pool.skaters (skater_id),
  constraint point_game_fk foreign key (point_game_id) references hockey_pool.nhl_game (game_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.team_points
(
  team_point_id number not null,
  team_point_point_id number not null,
  team_point_player_id number not null,
  constraint team_point_id_pk primary key (team_point_id),
  constraint team_point_point_fk foreign key (team_point_point_id) references hockey_pool.points (point_id),
  constraint team_point_player_fk foreign key (team_point_player_id) references hockey_pool.players (player_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.week_dates
(
  week_date_id number not null,
  week_date_week_id number not null,
  week_date_date date not null,
  constraint week_date_id_pk primary key (week_date_id),
  constraint week_date_week_fk foreign key (week_date_week_id) references hockey_pool.weeks (week_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.teams
(
  team_id number not null,
  team_skater_id number not null,
  team_player_id number not null,
  constraint team_id_pk primary key (team_id),
  constraint team_skater_fk foreign key (team_skater_id) references hockey_pool.skaters (skater_id),
  constraint team_player_fk foreign key (team_player_id) references hockey_pool.players (player_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

create table hockey_pool.activations
(
  activation_id number not null,
  activation_skater_id number not null,
  activation_player_id number not null,
  activation_position_id number not null,
  constraint activation_id_pk primary key (activation_id),
  constraint activation_skater_fk foreign key (activation_skater_id) references hockey_pool.skaters (skater_id),
  constraint activation_player_fk foreign key (activation_player_id) references hockey_pool.players (player_id),
  constraint activation_position_fk foreign key (activation_position_id) references hockey_pool.positions (position_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create table hockey_pool.activated_teams
(
  activated_team_id number not null,
  activated_team_skater_id number not null,
  activated_team_player_id number not null,
  activated_team_week_id number not null,
  activated_team_position_id number not null,
  constraint activated_team_id_pk primary key (activated_team_id),
  constraint activated_team_skater_fk foreign key (activated_team_skater_id) references hockey_pool.skaters (skater_id),
  constraint activated_team_player_fk foreign key (activated_team_player_id) references hockey_pool.players (player_id),
  constraint activated_team_week_fk foreign key (activated_team_week_id) references hockey_pool.weeks (week_id),
  constraint activated_team_position_fk foreign key (activated_team_position_id) references hockey_pool.positions (position_id)
)
tablespace APEX
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create sequence hockey_pool.draft_round_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.weeks_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.pools_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.skater_positions_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.positions_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.hockey_team_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.skaters_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.nhl_game_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.injuries_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.players_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.draft_picks_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.matches_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.points_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.team_points_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.week_dates_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.teams_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.activations_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
create sequence hockey_pool.activated_teams_seq minvalue 1 maxvalue 100000000000000 start with 1 increment by 1 cache 20;
 
CREATE OR REPLACE TRIGGER hockey_pool.bi_draft_round
  before insert on hockey_pool.draft_round
  for each row  
begin   
  if :NEW.round_id is null then 
    select hockey_pool.draft_round_seq.nextval into :NEW.round_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_weeks
  before insert on hockey_pool.weeks  
  for each row  
begin   
  if :NEW.week_id is null then 
    select hockey_pool.weeks_seq.nextval into :NEW.week_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_pools
  before insert on hockey_pool.pools
  for each row 
begin   
  if :NEW.pool_id is null then 
    select hockey_pool.pools_seq.nextval into :NEW.pool_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_positions
  before insert on hockey_pool.positions
  for each row 
begin   
  if :NEW.position_id is null then 
    select hockey_pool.positions_seq.nextval into :NEW.position_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_hockey_team
  before insert on hockey_pool.hockey_team
  for each row 
begin   
  if :NEW.hockey_team_id is null then 
    select hockey_pool.hockey_team_seq.nextval into :NEW.hockey_team_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_skaters
  before insert on hockey_pool.skaters
  for each row 
begin   
  if :NEW.skater_id is null then 
    select hockey_pool.skaters_seq.nextval into :NEW.skater_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_nhl_game
  before insert on hockey_pool.nhl_game
  for each row 
begin   
  if :NEW.game_id is null then 
    select hockey_pool.nhl_game_seq.nextval into :NEW.game_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_injuries
  before insert on hockey_pool.injuries
  for each row 
begin   
  if :NEW.injury_id is null then 
    select hockey_pool.injuries_seq.nextval into :NEW.injury_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_players
  before insert on hockey_pool.players
  for each row 
begin   
  if :NEW.player_id is null then 
    select hockey_pool.players_seq.nextval into :NEW.player_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_draft_picks
  before insert on hockey_pool.draft_picks
  for each row 
begin   
  if :NEW.pick_id is null then 
    select hockey_pool.draft_picks_seq.nextval into :NEW.pick_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_matches
  before insert on hockey_pool.matches
  for each row 
begin   
  if :NEW.match_id is null then 
    select hockey_pool.matches_seq.nextval into :NEW.match_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_points
  before insert on hockey_pool.points
  for each row 
begin   
  if :NEW.point_id is null then 
    select hockey_pool.points_seq.nextval into :NEW.point_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_team_points
  before insert on hockey_pool.team_points
  for each row 
begin   
  if :NEW.team_point_id is null then 
    select hockey_pool.team_points_seq.nextval into :NEW.team_point_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_week_dates
  before insert on hockey_pool.week_dates
  for each row 
begin   
  if :NEW.week_date_id is null then 
    select hockey_pool.week_dates_seq.nextval into :NEW.week_date_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_teams
  before insert on hockey_pool.teams
  for each row 
begin   
  if :NEW.team_id is null then 
    select hockey_pool.teams_seq.nextval into :NEW.team_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_activated_teams
  before insert on hockey_pool.activated_teams
  for each row 
begin   
  if :NEW.activated_team_id is null then 
    select hockey_pool.activated_teams_seq.nextval into :NEW.activated_team_id from dual; 
  end if; 
end;
/

CREATE OR REPLACE TRIGGER hockey_pool.bi_activations
  before insert on hockey_pool.activations
  for each row 
begin   
  if :NEW.activation_id is null then 
    select hockey_pool.activations_seq.nextval into :NEW.activation_id from dual; 
  end if; 
end;
/

spool off;

