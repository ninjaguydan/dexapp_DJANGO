from django import template
from main_app.models import Pokemon

register = template.Library()

#Given a pokemon's ID, return the average of all pokemon's ratings
def rating_avg(value):
    pkmn = Pokemon.objects.get(id = value)
    if pkmn.reviews.all():
        avg = Pokemon.objects.rating_avg(value)
    else:
        avg = 0
    return round(avg, 2)
register.filter('rating_avg', rating_avg)


def check_zero(value):
    if value == 0:
        return "-"
    else:
        return value
register.filter('check_zero', check_zero)
