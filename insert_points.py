from game import Game
import settings
import vars
import cx_Oracle

con = cx_Oracle.connect('hockey_pool/' + settings.password + '@' + settings.database)
c = con.cursor()

for s in vars.seasons:
    for i in range(1, s["games"]+1):
        g = Game("02", str(i).zfill(4), s["year"])
        print g.seasonID, g.gameID, g.yearID[0:4]
        try:
            for k,v in g.homeTeamSkaters.iteritems():
                proc_vars = [g.seasonID, g.gameID, g.yearID[0:4], v["nhl_id"],v["goals"],v["assists"],v["plusminus"],v["shorthandedgoals"],v["shorthandedassists"],v["gamewinningassists"],v["emptynetassists"],v["powerplaygoals"],v["powerplayassists"],v["gamewinninggoals"],v["penaltyshotgoals"],v["emptynetgoals"],v["pims"],v["pimsdrawn"],v["hits"],v["shots"],v["blockedshots"],v["misses"],v["blocks"],v["fights"],v["giveaways"],v["takeaways"],v["faceoffwins"],v["faceofflosses"],"'" + str(v["timeonice"]) + "'",v["shootoutgoals"],v["shootoutmisses"],v["wins"],v["otlosses"],v["saves"],v["shutouts"],v["penaltyshotsaves"],v["penaltyshotgoalsagainst"],v["shootoutsaves"],v["shootoutgoalsagainst"],v["goalsagainst"],v["firststars"],v["secondstars"],v["thirdstars"]]
                c.callproc('pkg_pool.insert_point', proc_vars)

            for k,v in g.awayTeamSkaters.iteritems():
                proc_vars = [g.seasonID, g.gameID, g.yearID[0:4], v["nhl_id"],v["goals"],v["assists"],v["plusminus"],v["shorthandedgoals"],v["shorthandedassists"],v["gamewinningassists"],v["emptynetassists"],v["powerplaygoals"],v["powerplayassists"],v["gamewinninggoals"],v["penaltyshotgoals"],v["emptynetgoals"],v["pims"],v["pimsdrawn"],v["hits"],v["shots"],v["blockedshots"],v["misses"],v["blocks"],v["fights"],v["giveaways"],v["takeaways"],v["faceoffwins"],v["faceofflosses"],"'" + str(v["timeonice"]) + "'",v["shootoutgoals"],v["shootoutmisses"],v["wins"],v["otlosses"],v["saves"],v["shutouts"],v["penaltyshotsaves"],v["penaltyshotgoalsagainst"],v["shootoutsaves"],v["shootoutgoalsagainst"],v["goalsagainst"],v["firststars"],v["secondstars"],v["thirdstars"]]
                c.callproc('pkg_pool.insert_point', proc_vars)
        except cx_Oracle.IntegrityError, exception:
            error, = exception
            print proc_vars
            print "Oracle error code: ", error.code
            print "Oracle error message: ", error.message
        if i == 10:
            break;

    con.commit()

con.close()
