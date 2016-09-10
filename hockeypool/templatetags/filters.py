from django import template
from hockeypool.models import *

register = template.Library()

@register.simple_tag
def print_teams():
	rval = ""
	p = Player.objects.all().order_by("id")
	for x in p:
		rval += '<ul><li><a href="/team/%s/">%s</a></li></ul>' % (x.id, x.name)
	return rval

@register.simple_tag
def get_teams():
	rval = ""
	p = Player.objects.all().order_by("id")
	for x in p:
		rval += '<li><a href="/team/%s/">%s</a></li>' % (x.id, x.name)
	return rval

@register.simple_tag
def get_theme():
	p = Player.objects.get(id=request.user.id)
	return p.theme
