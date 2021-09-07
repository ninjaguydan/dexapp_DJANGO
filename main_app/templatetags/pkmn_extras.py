from django import template
from main_app.models import Pokemon, Type

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

def num_to_type(value):
    return Type.objects.get(id = value).name
register.filter('num_to_type', num_to_type)

def team_filler(team):
    if len(team) < 6:
        new = []
        for obj in team:
            new.append(obj)
        for item in range(6 - len(team)):
            new.append(0)
        return new
    else:
        return team
register.filter('team_filler', team_filler)

#Get dictionary items one by one because I'm too frustrated to figure out a simpler way to do this
def get_username(dictionary, key):
    return dictionary[key].added_by.username
register.filter('get_username', get_username)

def get_sprite(dictionary, key):
    return dictionary[key].pkmn.sprite_url
register.filter('get_sprite', get_sprite)

def get_user_img(dictionary, key):
    return dictionary[key].added_by.user_img.url
register.filter('get_user_img', get_user_img)