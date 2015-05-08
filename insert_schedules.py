#!/usr/bin/python
# -*- coding: utf-8 -*-

import vars
import unicodedata
import urllib2
from datetime import datetime
from parsers import seasonParser

def processTeamName(team):
    return vars.cityToID[team.decode('UTF-8', errors='strict').encode("ascii", "backslashreplace").replace("\\xe9", "e").upper()]

def formatDate(date):
    return datetime.strptime("Sat Apr 7, 2012", "%a %b %d, %Y").strftime("%d-%b-%Y").lstrip("0")

seasons = ["20112012", "20122013", "20132014", "20142015"]

for s in seasons:
    resp = urllib2.urlopen("http://www.nhl.com/ice/schedulebyseason.htm?season=" + s  + "&gameType=2&team=&network=&venue=")
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
                            print '"%s", "%s", "%s", "%s"' %(formatDate(x[0]),processTeamName(x[2]),processTeamName(x[3]),s[0:4]+"02"+str(count).zfill(4))
                            count += 1

