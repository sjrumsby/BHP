import django
import os
import sys

if "/var/www/django/bhp" not in sys.path:
        sys.path.append("/var/www/django/bhp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp.settings")
django.setup()

import vars
from hockeypool.models import *

if len(sys.argv) != 2:
	print "Invalid command"
	exit()

if sys.argv[1] == "-d" or sys.argv[1] == "--daily":
	#Do some shit to get the current date here
	daily_update()

elif sys.argv[1] == "-w" or sys.argv[1] == "--weekly":
	#Do some shit to get the current date here
	weekly_update()

elif sys.argv[1] == "-f" or sys.argv[1] == "--full":
	#Do some shit to get the current date here
	full_update()

elif sys.argv[1] == "-s" or sys.argv[1] == "--season":
	#Do some shit to get the current date here
	season_update()
else:
	print "Unknown flag"
