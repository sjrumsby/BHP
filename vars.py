#General Application information

version = "1.0"
author = "Sean Rumsby"
database = "data.sqlite"
debug = 0
concurrent = 10

#All of the play types and other data required to initialize database

hockey_teams = [
			(1, "ANA", "ANAHEIM DUCKS"),
			(2, "BOS", "BOSTON BRUINS"),
			(3, "BUF", "BUFFALO SABRES"),
			(4, "CGY", "CALGARY FLAMES"),
			(5, "CAR", "CAROLINA HURRICANES"),
			(6, "CHI", "CHICAGO BLACKHAWKS"),
			(7, "COL", "COLORADO AVALANCHE"),
			(8, "CBJ", "COLUMBUS BLUE JACKETS"),
			(9, "DAL", "DALLAS STARS"),
			(10, "DET", "DETROIT RED WINGS"),
			(11, "EDM", "EDMONTON OILERS"),
			(12, "FLA", "FLORIDA PANTHERS"),
			(13, "LAK", "LOS ANGELES KINGS"),
			(14, "MIN", "MINNESOTA WILD"),
			(15, "MTL", "MONTREAL CANADIENS"),
			(16, "NSH", "NASHVILLE PREDATORS"),
			(17, "NJD", "NEW JERSEY DEVILS"),
			(18, "NYI", "NEW YORK ISLANDERS"),
			(19, "NYR", "NEW YORK RANGERS"),
			(20, "OTT", "OTTAWA SENATORS"),
			(21, "PHI", "PHILADELPHIA FLYERS"),
			(22, "PHX", "PHOENIX COYOTES"),
			(23, "PIT", "PITTSBURGH PENGUINS"),
			(24, "SJS", "SAN JOSE SHARKS"),
			(25, "STL", "ST. LOUIS BLUES"),
			(26, "TBL", "TAMPA BAY LIGHTNING"),
			(27, "TOR", "TORONTO MAPLE LEAFS"),
			(28, "VAN", "VANCOUVER CANUCKS"),
			(29, "WSH", "WASHINGTON CAPITALS"),
			(30, "WPG", "WINNIPEG JETS")
		]
		
miss_types 	= [
				(1, "Crossbar"), 
				(2, "Over"), 
				(3, "Post"), 
				(4, "Tip"),
				(5, "Wide"),
				]
				
penl_types = [
				(1, "Boarding"),
				(2, "Broken stick"),
				(3, "Charging"),
				(4, "Clipping"),
				(5, "Closing hand on the puck"),
				(6, "Cross-checking"),
				(7, "Delay of game"),
				(8, "Elbowing"),
				(9, "Goalkeeper interference"),
				(10, "High-sticking"),
				(11, "Holding"),
				(12, "Holding the stick"),
				(13, "Hooking"),
				(14, "Illegal equipment"),
				(15, "Illegal stick"),
				(16, "Instigator"),
				(17, "Interference"),
				(18, "Kneeing"),
				(19, "Leaving penalty bench too early"),
				(20, "Leaving the crease (goalkeeper)"),
				(21, "Participating in the play beyond the center red line (goalkeeper)"),
				(22, "Roughing"),
				(23,"Slashing"),
				(24, "Throwing puck towards opponent's goal (goalkeeper)"),
				(25, "Throwing stick"),
				(26, "Tripping"),
				(27, "Unsportsmanlike conduct"),
				]

play_types 	= [
				(1, "BLOCK"), 
				(2, "FAC"),
				(3, "GIVE"),
				(4, "GOAL"),
				(5, "GEND"),
				(6, "HIT"),
				(7, "MISS"),
				(8, "PEND"),
				(9, "PENL"),
				(10, "PSTR"),
				(11, "SHOT"),
				(12, "STOP"),
				(13, "TAKE"),
				(14, "SOC"),
				(15, "EISTR"),
				(16, "EIEND"),
				(17, "GOFF"),
				]

shot_types 	= [
				(1, "Backhand"),
				(2, "Snap"),
				(3,"Slap"),
				(4, "Tip"),
				(5, "Wrap"),
				(6, "Wrist"),
				(7, "Deflected"),
				(8, "Tip-In"),
				(9, "Wrap-around"),
				(10, "Undefined"),
				]

stop_types 	= [
				(1, "Frozen"),
				(2, "Goalie"),
				(3, "Icing"),
				(4, "Hand Pass"),
				(5, "High Stick"), 
				(6, "Injury"),
				(7, "In Benches"), 
				(8, "In Crowd"),
				(9, "In Netting"), 
				(10, "Net Off"),
				(11, "TV Timeout"),
				(12, "Official Injury"),
				(13, "Offside"),
				(14, "Referee or Linesman"),
				(15, "Player Equipment"),
				(16, "Visitor Timeout"),
				(17, "Home Timeout"),
				(18, "Clock Problem"),
				(19, "Video Review"),
				(20, "Rink Repair"),
				]

strength_types = [
					(1, "SH"),
					(2, "EV"),
					(3, "PP"),
				]
				
zone_types 	= [
				(1, "Offensive"), 
				(2, "Neutral"),
				(3, "Defensive"),
				]
				
miss_types_reverse = dict((v,k) for k,v in miss_types)
penl_types_reverse = dict((v,k) for k,v in penl_types)
play_types_reverse = dict((v,k) for k,v in play_types)
shot_types_reverse = dict((v,k) for k,v in shot_types)
stop_types_reverse = dict((v,k) for k,v in stop_types)
zone_types_reverse = dict((v,k) for k,v in zone_types)
strength_types_reverse = dict((v,k) for k,v in strength_types)

#General data structures useful throughout Application

shortNameToID = {	"ANA" : 1,
					"ARI" : 22,
					"BOS" : 2,
					"BUF" : 3, 
					"CGY" : 4,
					"CAR" : 5,
					"CHI" : 6,
					"COL" : 7,
					"CBJ" : 8,
					"DAL" : 9,
					"DET" : 10,
					"EDM" : 11,
					"FLA" : 12,
					"LAK" : 13,
					"MIN" : 14,
					"MTL" : 15,
					"NSH" : 16,
					"NJD" : 17,
					"NYI" : 18,
					"NYR" : 19,
					"OTT" : 20,
					"PHI" : 21,
					"PHX" : 22,
					"PIT" : 23,
					"SJS" : 24,
					"STL" : 25,
					"TBL" : 26,
					"TOR" : 27,
					"VAN" : 28,
					"WSH" : 29,
					"WPG" : 30,
					"T.B" : 26,
					"L.A" : 13,
					"N.J" : 17
				}

longNameToID = {	"ANAHEIM DUCKS" : 1,
					"ARIZONA COYOTES" : 22,
					"BOSTON BRUINS" : 2,
					"BUFFALO SABRES" : 3,
					"CALGARY FLAMES" : 4,
					"CAROLINA HURRICANES" : 5,
					"CHICAGO BLACKHAWKS" : 6,
					"COLORADO AVALANCHE" : 7,
					"COLUMBUS BLUE JACKETS" : 8,
					"DALLAS STARS" : 9,
					"DETROIT RED WINGS" : 10,
					"EDMONTON OILERS" : 11,
					"FLORIDA PANTHERS" : 12,
					"LOS ANGELES KINGS" : 13,
					"MINNESOTA WILD" : 14,
					"MONTREAL CANADIENS" : 15,
					"NASHVILLE PREDATORS" : 16,
					"NEW JERSEY DEVILS" : 17,
					"NEW YORK ISLANDERS" : 18,
					"NEW YORK RANGERS" : 19,
					"OTTAWA SENATORS" : 20,
					"PHILADELPHIA FLYERS" : 21,
					"PHOENIX COYOTES" : 22,
					"PITTSBURGH PENGUINS" : 23,
					"SAN JOSE SHARKS" : 24,
					"ST. LOUIS BLUES" : 25,
					"TAMPA BAY LIGHTNING" : 26,
					"TORONTO MAPLE LEAFS" : 27,
					"VANCOUVER CANUCKS" : 28,
					"WASHINGTON CAPITALS" : 29,
					"WINNIPEG JETS" : 30,
				}
				

longNameToShortName = {	"ANAHEIM DUCKS" : "ANA",
						"ARIZONA COYOTES" : "ARI",
						"BOSTON BRUINS" : "BOS",
						"BUFFALO SABRES" : "BUF",
						"CALGARY FLAMES" : "CGY",
						"CAROLINA HURRICANES" : "CAR",
						"CHICAGO BLACKHAWKS" : "CHI",
						"COLORADO AVALANCHE" : "COL",
						"COLUMBUS BLUE JACKETS" : "CBJ",
						"DALLAS STARS" : "DAL",
						"DETROIT RED WINGS" : "DET",
						"EDMONTON OILERS" : "EDM",
						"FLORIDA PANTHERS" : "FLA",
						"LOS ANGELES KINGS" : "LAK",
						"MINNESOTA WILD" : "MIN",
						"MONTREAL CANADIENS" : "MTL",
						"NASHVILLE PREDATORS" : "NSH",
						"NEW JERSEY DEVILS" : "NJD",
						"NEW YORK ISLANDERS" : "NYI",
						"NEW YORK RANGERS" : "NYR",
						"OTTAWA SENATORS" : "OTT",
						"PHILADELPHIA FLYERS" : "PHI",
						"PHOENIX COYOTES" : "PHX",
						"PITTSBURGH PENGUINS" : "PIT",
						"SAN JOSE SHARKS" : "SJS",
						"ST. LOUIS BLUES" : "STL",
						"TAMPA BAY LIGHTNING" : "TBL",
						"TORONTO MAPLE LEAFS" : "TOR",
						"VANCOUVER CANUCKS" : "VAN",
						"WASHINGTON CAPITALS" : "WSH",
						"WINNIPEG JETS" : "WPG",
					}

cityToID = {
                "ANAHEIM" : 1,
                "ARIZONA" : 22,
                "BOSTON" : 2,
                "BUFFALO" : 3,
                "CALGARY" : 4,
                "CAROLINA" : 5,
                "CHICAGO" : 6,
                "COLORADO" : 7,
                "COLUMBUS" : 8,
                "DALLAS" : 9,
                "DETROIT" : 10,
                "EDMONTON" : 11,
                "FLORIDA" : 12,
                "LOS ANGELES" : 13,
                "MINNESOTA" : 14,
                "MONTREAL" : 15,
                "NASHVILLE" : 16,
                "NEW JERSEY" : 17,
                "NY ISLANDERS" : 18,
                "NY RANGERS" : 19,
                "OTTAWA" : 20,
                "PHILADELPHIA" : 21,
                "PHOENIX" : 22,
                "PITTSBURGH" : 23,
                "SAN JOSE" : 24,
                "ST. LOUIS" : 25,
                "TAMPA BAY" : 26,
                "TORONTO" : 27,
                "VANCOUVER" : 28,
                "WASHINGTON" : 29,
                "WINNIPEG" : 30,
            }

idToShortName = dict((v,k) for k,v in shortNameToID.iteritems())
idToLongName = dict((v,k) for k,v in longNameToID.iteritems())
shortNameToLongName = dict((v,k) for k,v in longNameToShortName.iteritems())
idToCity = dict((v,k) for k,v in cityToID.iteritems())

numberOfGames = { 	"20112012" : 1230,
					"20122013" : 624,
					"20132014" : 1230,
				}

seasons = [ {"year" : "20112012", "games" : 1230},
            {"year" : "20122013", "games" : 720},
            {"year" : "20132014", "games" : 1230},
            {"year" : "20142015", "games" : 1230}
          ]

