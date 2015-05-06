from game import Game

g = Game("02", "0001", "20142015")

for k,v in g.homeTeamSkaters.iteritems():
	print k
	for k2,v2 in g.homeTeamSkaters[k].iteritems():
		print "\t%s : %s" % (k2, v2)
	print "\n"