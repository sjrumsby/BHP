from django import template
from hockeypool.models import *

register = template.Library()

@register.simple_tag
def print_teams():
	teams = Player.objects.all().values_list("name", flat=True)
	return teams
