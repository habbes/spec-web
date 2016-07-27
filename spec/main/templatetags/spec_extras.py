
from django import template

register = template.Library()


@register.filter
def percentage(value):
    return '%.0f' %  (value * 100)


@register.filter
def profileskillscore(value, arg):
    ps = value.profileskill_set.get(profile=arg)
    return percentage(ps.normalized_skill_score)