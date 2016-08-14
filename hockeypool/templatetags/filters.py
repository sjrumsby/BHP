from django import template
from hockeypool.models import *
from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()

@register.filter(is_safe=True)
def print_teams():
	rval = ""
	p = Player.objects.all()
	for x in p:
		rval += '<ul><li><a href="/team/%s/">%s</a></li></ul>' % (x.id, x.name)
	return mark_safe(rval)

@register.filter(is_safe=True)
def get_teams():
	rval = ""
	p = Player.objects.all()
	for x in p:
		rval += '<li><a href="/team/%s/">%s</a></li>' % (x.id, x.name)
	return format_html(rval)

@register.simple_tag
def get_theme():
	p = Player.objects.get(id=request.user.id)
	return p.theme
