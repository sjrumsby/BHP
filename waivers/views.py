from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from hockeypool.models import *
from waivers.models import *

import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
        if request.method == "POST":
                action = "POST"
                waivers = Waiver.objects.filter(player_id = request.user.id).filter(state__lte=2)
                if len(waivers) > 2:
                        error = 1
                        error_msg = "You can only place 2 players on waivers per week"
                else:
                        player = request.POST.get('waiver_player')
			logger.info("%s is attempting to drop %s to waivers" % (request.user.id, player))
                        waiver = Waiver.objects.filter(skater_id = player).filter(state__lte=2)
                        if len(waiver) > 0:
                                error = 1
                                error_msg = "This player is already on waivers"
				logger.info("Player is already on waivers")
                        else:
                                error = 0
                                error_msg = "Success"
                                s = Skater.objects.get(nhl_id = player)
                                w = Waiver.objects.create(skater = s, player = Player.objects.get(pk=request.user.id), state = 0)
                                w.save()
				logger.info("Waiver successfully processed")
        else:
                action = "GET"
                error = 0
                error_msg = ""

        team = Team.objects.filter(player = request.user.id)
        skater_ids = team.values_list("skater_id", flat="True")
        all_waivers = Waiver.objects.filter(state__lte=2)
        player_waivers = Waiver.objects.filter(skater_id__in = skater_ids).filter(state__lte=2)
        all_pickups = Waiver_Pickup.objects.filter(state=1)
	player_pickups = Waiver_Pickup.objects.filter(state=0).filter(player=request.user.id)
        context = { 'page_name' : 'Waivers', 'team' : team, 'all_waivers' : all_waivers, 'player_waivers' : player_waivers, 'error' : error, 'error_msg' : error_msg, 'action' : action, 'pickups' : all_pickups, 'player_pickups' : player_pickups}
        return render(request, 'waivers/index.html', context)

@login_required
def waiver_cancel(request, waiver_id):
        if Waiver.objects.filter(id = waiver_id).exists():
                waiver = Waiver.objects.get(id = waiver_id)
                p = Player.objects.get(id = request.user.id)
                logger.info("%s is attempting to cancel waiver drop of skater %s" % (p.name, waiver.skater.first_name + ' ' + waiver.skater.last_name))
                if waiver.player == p:
                        if waiver.state == 0:
                                logger.info("Success")
                                waiver.delete()
                                error = 0
                                error_msg = "Success"
                        else:
                                error = 1
                                error_msg = "Player has already cleared waivers... can no longer be cancelled"
                                logger.info("Failed because the skater has already cleared waivers")
                else:
                        logger.info("Attempt failed as the user attempting did not initiate")
                        error = 1
                        error_msg = "You are not the GM of this player - you cannot cancel it"
        else:
                error = 1
                error_msg = "Could not find waiver with id: %s" % waiver_id
        context = { 'page_name' : "Waiver Cancel", 'error' : error, 'msg' : error_msg }
        return render(request, 'waivers/cancel.html', context)

@login_required
def waiver_add(request):
	error = 0
        if request.method == "POST":
                p = Player.objects.get(id = request.user.id)
                logger.info("%s is trying to claim %s (%s) off of waivers" % (p.name, request.POST.get("waiver_add_id"), request.POST.get('waiver_add')))
                nhl_id = request.POST.get("waiver_add_id")

		if not nhl_id.isnumeric():
			name = request.POST.get("waiver_add")
			if Skater.objects.filter(full_name=name).count() == 1:
				s = Skater.objects.get(full_name=name)
				nhl_id = s.nhl_id
				logger.info("Found player nhl_id: %s from name: %s" % (nhl_id, name))
			else:
				if Skater.objects.filter(full_name__iexact=name).count() == 1:
					s = Skater.objects.get(full_name__iexact=name)
					nhl_id = s.nhl_id
					logger.info("Found player nhl_id: %s from name: %s" % (nhl_id, name))
				else:
					error = 1
					error_msg = "No player found with name: %s" % name
					logger.info("No player found with name: %s" % name)

		if error != 1:
			if Skater.objects.filter(nhl_id = nhl_id).exists():
				s = Skater.objects.get(nhl_id = nhl_id)
				logger.info("%s is trying to claim %s off of waivers" % (p.name, s.first_name + " " + s.last_name))
				t = Team.objects.all().values_list("skater_id", flat="True")
				if s.nhl_id in t:
					error = 1
					error_msg = "The player you are trying to claim is already owned"
					logger.info("Attempt failed because the player is owned by someone else")
				else:
					t = Team.objects.filter(player = p).count()
					if t >= 20:
						error = 1
						error_msg = "You cannot add a player without having a player clear waivers first"
						logger.info("The attempt failed because the manager already has 20 players")
					else:
						error = 0
						error_msg = ""
						logger.info("success")
						t = Team.objects.create(player = p, skater = s)
						t.save()
			else:
				error = 1
				error_msg = "The skater with id %s does not exist" % nhl_id
        else:
                error = 1
                error_msg = "You didn't POST any data... quit fucking with my shit"
        context = { 'page_name' : "Waiver Add", 'error' : error, 'msg' : error_msg }
        return render(request, 'waivers/add.html', context)

