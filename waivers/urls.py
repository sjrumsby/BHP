@login_required
def waivers(request):
        if request.method == "POST":
                action = "POST"
                waivers = Waiver.objects.filter(player_id = request.user.id).filter(state__lte=2)
                if len(waivers) > 2:
                        error = 1
                        error_msg = "You can only place 2 players on waivers per week"
                else:
                        player = request.POST.get('waiver_player')
                        waiver = Waiver.objects.filter(skater_id = player).filter(state__lte=2)
                        if len(waiver) > 0:
                                error = 1
                                error_msg = "This player is already on waivers"
                        else:
                                error = 0
                                error_msg = "Success"
                                s = Skater.objects.get(id = player)
                                w = Waiver.objects.create(skater = s, player = Player.objects.get(pk=request.user.id), state = 0)
                                w.save()
        else:
                action = "GET"
                error = 0
                error_msg = ""

        team = Team.objects.filter(player = request.user)
        skater_ids = team.values_list("skater_id", flat="True")
        all_waivers = Waiver.objects.filter(state__lte=2)
        player_waivers = Waiver.objects.filter(skater_id__in = skater_ids).filter(state__lte=2)
        pickups = Waiver_Pickup.objects.filter(state=0)
        context = { 'page_name' : 'Waivers', 'team' : team, 'all_waivers' : all_waivers, 'player_waivers' : player_waivers, 'error' : error, 'error_msg' : error_msg, 'action' : action, 'pickups' : pickups }
        return render(request, 'hockeypool/waivers.html', context)

@login_required
def waiver_cancel(request, waiver_id):
        if Waiver.objects.filter(id = waiver_id).exists():
                waiver = Waiver.objects.get(id = waiver_id)
                p = Player.objects.get(id = request.user.id)
                logger.info("%s is attempting to cancel waiver drop of skater %s" % (p.name, waiver.skater.name))
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
        return render(request, 'hockeypool/waiver_cancel.html', context)

@login_required
def waiver_add(request):
        if request.method == "POST":
                p = Player.objects.get(id = request.user.id)
                nhl_id = request.POST.get("waiver_add_id")
                if Skater.objects.filter(nhl_id = nhl_id).exists():
                        s = Skater.objects.get(nhl_id = nhl_id)
                        logger.info("%s is trying to claim %s off of waivers" % (p.name, s.name))
                        t = Team.objects.all().values_list("skater_id", flat="True")
                        if s.id in t:
                                error = 1
                                error_msg = "The player you are trying to claim is already owned"
                                logger.info("Attempt failed because the player is owned by someone else")
                        else:
                                t = Team.objects.filter(player = p).count()
                                if t >= 19:
                                        error = 1
                                        error_msg = "You cannot add a player without having a player clear waivers first"
                                        logger.info("The attempt failed because the manager already has 19 players")
                                else:
                                        error = 0
                                        error_msg = ""
                                        logger.info("success")
                                        new_t = Team.objects.create(player = p, skater = s, week = 1, active = 0)
                                        new_t.save()
                                        new_wp = Waiver_Pickup.objects.create(player = p, skater = s)
                                        new_wp.save()
                else:
                        error = 1
                        error_msg = "The skater with id %s does not exist" % nhl_id
        else:
                error = 1
                error_msg = "You didn't POST any data... quit fucking with my shit"
        context = { 'page_name' : "Waiver Add", 'error' : error, 'msg' : error_msg }
        return render(request, 'hockeypool/waiver_add.html', context)

