from django import template

register = template.Library()

@register.simple_tag
def print_teams():
	return "Pancakes!"
