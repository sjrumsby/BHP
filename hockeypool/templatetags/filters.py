from django import template
from hockeypool.models import *

register = template.Library()

@register.simple_tag
def print_teams():
	rval = ""
	p = Player.objects.all()
	for x in p:
		rval += '<ul><li><a href="/team/%s/">%s</a></li></ul>' % (x.id, x.name)
	return rval
