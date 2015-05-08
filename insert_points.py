from game import Game
import settings
import cx_Oracle
con = cx_Oracle.connect('hockey_pool/P4nc4k3s_devl@localhost')
c = con.cursor()

for i in range (1,11):
    g = Game("02", str(i).zfill(4), "20142015")
    print g.seasonID, g.gameID, g.yearID[0:4]
    
    for k,v in g.homeTeamSkaters.iteritems():
        c.callproc('pkg_pool.insert_point', (g.seasonID, g.gameID, g.yearID[0:4], v["nhl_id"],v["goals"],v["assists"],v["plusminus"],v["shorthandedgoals"],v["shorthandedassists"],v["gamewinningassists"],v["emptynetassists"],v["powerplaygoals"],v["powerplayassists"],v["gamewinninggoals"],v["penaltyshotgoals"],v["emptynetgoals"],v["pims"],v["pimsdrawn"],v["hits"],v["shots"],v["blockedshots"],v["misses"],v["blocks"],v["fights"],v["giveaways"],v["takeaways"],v["faceoffwins"],v["faceofflosses"],"'" + str(v["timeonice"]) + "'",v["shootoutgoals"],v["shootoutmisses"],v["wins"],v["otlosses"],v["saves"],v["shutouts"],v["penaltyshotsaves"],v["penaltyshotgoalsagainst"],v["shootoutsaves"],v["shootoutgoalsagainst"],v["goalsagainst"],v["firststars"],v["secondstars"],v["thirdstars"]))

    for k,v in g.awayTeamSkaters.iteritems():
        c.callproc('pkg_pool.insert_point', (g.seasonID, g.gameID, g.yearID[0:4], v["nhl_id"],v["goals"],v["assists"],v["plusminus"],v["shorthandedgoals"],v["shorthandedassists"],v["gamewinningassists"],v["emptynetassists"],v["powerplaygoals"],v["powerplayassists"],v["gamewinninggoals"],v["penaltyshotgoals"],v["emptynetgoals"],v["pims"],v["pimsdrawn"],v["hits"],v["shots"],v["blockedshots"],v["misses"],v["blocks"],v["fights"],v["giveaways"],v["takeaways"],v["faceoffwins"],v["faceofflosses"],"'" + str(v["timeonice"]) + "'",v["shootoutgoals"],v["shootoutmisses"],v["wins"],v["otlosses"],v["saves"],v["shutouts"],v["penaltyshotsaves"],v["penaltyshotgoalsagainst"],v["shootoutsaves"],v["shootoutgoalsagainst"],v["goalsagainst"],v["firststars"],v["secondstars"],v["thirdstars"]))

con.commit()
con.close()
