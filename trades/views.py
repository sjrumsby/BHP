from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q

from hockeypool.models import *
from trades.models import *
import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
        in_trades = Trade.objects.filter(player2__id = request.user.id)
        out_trades = Trade.objects.filter(player1__id = request.user.id)
        if len(in_trades) > 0:
                t_in = 1
        else:
                t_in = 0

        if len(out_trades) > 0:
                t_out = 1
        else:
                t_out = 0
        all_trades = Trade.objects.filter(state=1)
        prev_trades = Trade.objets.filter(state=1).filter(Q(player1__id=request.user.id) | Q(player2__id=request.user.id))
        main = {'t_in' : t_in, 't_out' : t_out, 'in_trades' : in_trades, 'out_trades' : out_trades, 'all_trades' : all_trades}
        side = {'prev_trades' : prev_trades }
        context = { 'page_name' : 'Trades', 'main' : main, 'side' : side }
        return render(request, 'trades/index.html', context)

@login_required
def trade_cancel(request, trade_id):
        logger.info("User: %s is attempting to cancel trade: %s" % (request.user.id, trade_id))
        if Trade.objects.filter(id=trade_id).exists():
                t = Trade.objects.get(id=trade_id)
                if t.player1.id == request.user.id:
                        logger.info("Player initiated the request, cancelling trade")
                        t.delete()
                        error = 0
                        errors = ""
                elif t.player2.id == request.user.id:
                        logger.info("Player has been requested this trade, cancelling trade")
                        t.delete()
                        error = 0
                        errors = ""
                else:
                        logger.info("Player does not have the right to cancel this trade")
                        errors = 1
                        error = "You are not involved in this trade, you cannot cancel it"

        else:
                logger.info("Trade does not exist")
                errors = 1
                error = "Trade with id: %s does not exist" % trade_id
        main = { 'error' : error, 'errors' : errors }
        side = None
        context = { 'page_name' : 'Cancel Trade', 'main' : main, 'side' : side }
        return render(request, 'trades/cancel.html', context)


@login_required
def trade_accept(request, trade_id):
        logger.info("User: %s is attempting to accept trade: %s" % (request.user.id, trade_id))
        if Trade.objects.filter(id=trade_id).exists():
                t = Trade.objects.get(id=trade_id)
                if t.player2.id == request.user.id:
                        logger.info("Player initiated the request, accepting trade")
                        if Team.objects.filter(skater = t.skater1).exists() and Team.objects.filter(skater = t.skater2).exists():
                                t1 = Team.objects.get(skater = t.skater1)
                                t2 = Team.objects.get(skater = t.skater2)
                                team_1 = t1.player
                                team_2 = t2.player
                                t1.player = team_2
                                t2.player = team_1
                                t1.save()
                                t2.save()
                                error = 0
                                errors = 0
                        else:
                                logger.info("One of the players involved in the trade is no longer on any team")
                                errors = 1
                                error = "Someone involved in this trade no longer has the player on their tema, or something else went wrong. Contact the commissioner"

                        t.state = 1
                        t.save()
                else:
                        logger.info("Player does not have the right to accept this trade")
                        errors = 1
                        error = "You are not involved in this trade, you cannot cancel it"

        else:
                logger.info("Trade does not exist")
                errors = 1
                error = "Trade with id: %s does not exist" % trade_id
        main = { 'error' : error, 'errors' : errors }
        side = None
        context = { 'page_name' : 'Accept Trade', 'main' : main, 'side' : side }
        return render(request, 'trades/accept.html', context)


