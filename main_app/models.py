from django.db import models
from login_app.models import User
import requests


class PokeManager(models.Manager):
    def create_pkmn(self, index):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{index}/")
        return self.create(
            name = response.json()["name"],
            sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{index}.png",
            shiny_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{index}.png",
            art_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{index}.png",
            hp = response.json()['stats'][0]['base_stat'],
            attack = response.json()['stats'][1]['base_stat'],
            defense = response.json()['stats'][2]['base_stat'],
            sp_attack = response.json()['stats'][3]['base_stat'],
            sp_defense = response.json()['stats'][4]['base_stat'],
            speed = response.json()['stats'][5]['base_stat']
        )
    def add_types(self, index):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{index}/")
        current_pkmn = Pokemon.objects.get(id = index)
        for t in response.json()['types']:
            type_to_add = Type.objects.get(name = t['type']['name'])
            current_pkmn.types.add(type_to_add)

    def add_weaknesses(self, index):
        pkmn = Pokemon.objects.get(id = index)
        type1 = pkmn.types.all()[0]
        for weakness in type1.weak_to.all():
            pkmn.weak_to.add(weakness)
        for resistance in type1.resists.all():
            pkmn.resists.add(resistance)
        for immunity in type1.immune_to.all():
            pkmn.immune_to.add(immunity)
        if len(pkmn.types.all()) == 2:
            type2 = pkmn.types.all()[1]
            for weakness in type2.weak_to.all():
                if weakness in pkmn.resists.all():
                    pkmn.resists.remove(weakness)
                elif weakness not in pkmn.immune_to.all():
                    pkmn.weak_to.add(weakness)
                else:
                    break
            for resistance in type2.resists.all():
                if resistance in pkmn.weak_to.all():
                    pkmn.weak_to.remove(resistance)
                elif resistance not in type1.weak_to.all():
                    pkmn.resists.add(resistance)
                else:
                    break
            for immunity in type2.immune_to.all():
                if immunity in pkmn.weak_to.all():
                    pkmn.weak_to.remove(immunity)
                    pkmn.immune_to.add(immunity)
                elif immunity in pkmn.resists.all():
                    pkmn.resists.remove(immunity)
                    pkmn.immune_to.add(immunity)
                else:
                    pkmn.immune_to.add(immunity)


    def rating_avg(self, pkmn_id):
        pkmn = Pokemon.objects.get(id = pkmn_id)
        total = 0
        for review in pkmn.reviews.all():
            total += review.rating
        avg = total/len(pkmn.reviews.all())
        return round(avg, 2)


class TypeManager(models.Manager):
    def create_type(self, index):
        response = requests.get(f"https://pokeapi.co/api/v2/type/{index}/")
        return self.create(
            name = response.json()['name']
        )
    def add_relation(self, index):
        response = requests.get(f"https://pokeapi.co/api/v2/type/{index}/")
        current_type = Type.objects.get(id = index)
        #add weaknesses
        if response.json()['damage_relations']['double_damage_from']:
            for weakness in response.json()['damage_relations']['double_damage_from']:
                type_to_add = Type.objects.get(name = weakness['name'])
                current_type.weak_to.add(type_to_add)
        #add resistances
        if response.json()['damage_relations']['half_damage_from']:
            for resistance in response.json()['damage_relations']['half_damage_from']:
                type_to_add = Type.objects.get(name = resistance['name'])
                current_type.resists.add(type_to_add)
        #add immunitites
        if response.json()['damage_relations']['no_damage_from']:
            for immunity in response.json()['damage_relations']['no_damage_from']:
                type_to_add = Type.objects.get(name = immunity['name'])
                current_type.immune_to.add(type_to_add)

class Pokemon(models.Model):
    name = models.CharField(max_length=200, null = True)
    sprite_url = models.CharField(max_length=200, null = True)
    shiny_url = models.CharField(max_length=200, null = True)
    art_url = models.CharField(max_length=200, null = True)
    hp = models.IntegerField(null = True)
    attack = models.IntegerField(null = True)
    defense = models.IntegerField(null = True)
    sp_attack = models.IntegerField(null = True)
    sp_defense = models.IntegerField(null = True)
    speed = models.IntegerField(null = True)
    favorited_by = models.ManyToManyField(User, related_name = "favorites")
    weak_to = models.ManyToManyField('main_app.Type', related_name = "weak_pkmn")
    resists = models.ManyToManyField('main_app.Type', related_name = "resistant_pkmn")
    immune_to = models.ManyToManyField('main_app.Type', related_name = "immune_pkmn")
    objects = PokeManager()

class Type(models.Model):
    name = models.CharField(max_length=50, null=True)
    pkmn = models.ManyToManyField(Pokemon, related_name = "types")
    weak_to = models.ManyToManyField("self", symmetrical = False, related_name = "strong_against")
    resists = models.ManyToManyField("self", symmetrical = False, related_name = "weak_against")
    immune_to = models.ManyToManyField("self", symmetrical = False, related_name = "no_effect_on")
    objects = TypeManager()

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    added_by = models.ForeignKey(User, related_name = "reviews_added", null = True, on_delete = models.CASCADE)
    pkmn = models.ForeignKey(Pokemon, related_name = "reviews", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)