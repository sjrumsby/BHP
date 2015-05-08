#!/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import settings
import vars
import urllib2
from datetime import datetime
from parsers import playerParser

con = cx_Oracle.connect('hockey_pool/' + settings.password + '@' + settings.database)
c = con.cursor()

for s in vars.seasons:
    print "Adding players from season: %s" % s["year"]
    for i in range (1,35):
        resp = urllib2.urlopen("http://www.nhl.com/stats/historical?season="+s["year"]+"&gameType=2&team=&position=S&country=&pg=" + str(i))
        html = resp.read()
        p = playerParser()
        p.feed(html)

        for x in p.player:
            print x[1], x[2], vars.shortNameToID[x[3].split(", ")[-1]]
            c.callproc('pkg_pool.insert_skater', (x[1], x[2], vars.shortNameToID[x[3].split(", ")[-1]]))

    for i in range (1,5):
        resp = urllib2.urlopen("http://www.nhl.com/stats/historical?season="+s["year"]+"&gameType=2&team=&position=G&country=&pg=" + str(i))
        html = resp.read()
        p = playerParser()
        p.feed(html)

        for x in p.player:
            print x[1], x[2], vars.shortNameToID[x[3].split(", ")[-1]]
            c.callproc('pkg_pool.insert_skater', (x[1], x[2], vars.shortNameToID[x[3].split(", ")[-1]]))
    con.commit()

    print "Finished adding players from season: %s" % s["year"]
con.close()
