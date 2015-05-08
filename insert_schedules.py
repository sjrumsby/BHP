#!/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import settings
import vars
import unicodedata
import urllib2
from datetime import datetime
from parsers import seasonParser

def processTeamName(team):
    return vars.cityToID[team.decode('UTF-8', errors='strict').encode("ascii", "backslashreplace").replace("\\xe9", "e").upper()]

def formatDate(date):
    return datetime.strptime(date, "%a %b %d, %Y").strftime("%d-%b-%Y").lstrip("0")

con = cx_Oracle.connect('hockey_pool/' + settings.password + '@' + settings.database)
c = con.cursor()

for s in vars.seasons:
    print "Starting season: %s" % s["year"]
    resp = urllib2.urlopen("http://www.nhl.com/ice/schedulebyseason.htm?season=" + s["year"] + "&gameType=2&team=&network=&venue=")
    html = resp.read()
    p = seasonParser()
    p.feed(html)

    count = 1
    for x in p.games:
            if len(x) > 2:
                    #A whole lot of random bullshit to deal with NHL AllStar Games
                    if "Chara" not in x[2] and "Team Toews" not in x[2]:
                        #A whole bunch more bullshit to deal with the Olympics
                        if "Austria" not in x[2] and "Canada" not in x[2] and "Czech Republic" not in x[2] and "Finland" not in x[2] and "Latvia" not in x[2] and "Norway" not in x[2] and "Russia" not in x[2] and "Slovakia" not in x[2] and "Slovenia" not in x[2] and "Sweden" not in x[2] and "Switzerland" not in x[2] and "United States" not in x[2]:
                            print formatDate(x[0]),processTeamName(x[2]),processTeamName(x[3]),s["year"][0:4]+"02"+str(count).zfill(4)
                            c.callproc('pkg_pool.insert_nhl_game', (formatDate(x[0]),processTeamName(x[2]),processTeamName(x[3]),s["year"][0:4]+"02"+str(count).zfill(4)))
                            count += 1
    con.commit()

    print "Finished season: %s" % s["year"]
con.close()
