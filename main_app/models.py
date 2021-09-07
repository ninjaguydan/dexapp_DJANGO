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
    def add_gen(self, index):
        pkmn = Pokemon.objects.get(id = index)
        if pkmn.id < 152:
            pkmn.gen = 1
        elif pkmn.id < 252:
            pkmn.gen = 2
        elif pkmn.id < 387:
            pkmn.gen = 3
        elif pkmn.id < 494:
            pkmn.gen = 4
        elif pkmn.id < 650:
            pkmn.gen = 5
        elif pkmn.id < 722:
            pkmn.gen = 6
        elif pkmn.id < 810:
            pkmn.gen = 7
        else:
            pkmn.gen = 8
        pkmn.save()

    def add_types(self, index):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{index}/")
        current_pkmn = Pokemon.objects.get(id = index)
        for t in response.json()['types']:
            type_to_add = Type.objects.get(name = t['type']['name'])
            current_pkmn.types.add(type_to_add)

    def add_weaknesses(self, index):
        pkmn = Pokemon.objects.get(id = index)
        type1 = pkmn.types.all()[0]
        #add all of type1's weaknesses to Pokemon's weaknesses
        for weakness in type1.weak_to.all():
            pkmn.weak_to.add(weakness)
        #add all of type1's resistances to Pokemon's resistances
        for resistance in type1.resists.all():
            pkmn.resists.add(resistance)
        #add all of type1's immunites to Pokemon's immunities
        for immunity in type1.immune_to.all():
            pkmn.immune_to.add(immunity)
        #if a second type exists...
        if len(pkmn.types.all()) == 2:
            type2 = pkmn.types.all()[1]
            for weakness in type2.weak_to.all():
                #if type2's weakness is in Pokemon's resistances, remove resistance
                if weakness in pkmn.resists.all():
                    pkmn.resists.remove(weakness)
                #if type2's weakness isn't in Pokemon's immunities, add weakness to Pokemon
                elif weakness not in pkmn.immune_to.all():
                    pkmn.weak_to.add(weakness)
                else:
                    break
            for resistance in type2.resists.all():
                #if type2's resistance is in Pokemon's weaknesses, remove weakness
                if resistance in pkmn.weak_to.all():
                    pkmn.weak_to.remove(resistance)
                #if type2's resistance is not in type1's weaknesses, add resistance 
                elif resistance not in type1.weak_to.all():
                    pkmn.resists.add(resistance)
                else:
                    break
            for immunity in type2.immune_to.all():
                #if type2 immunity in Pokemon's weaknesses, remove weakness and add immunity
                if immunity in pkmn.weak_to.all():
                    pkmn.weak_to.remove(immunity)
                    pkmn.immune_to.add(immunity)
                #if type2 immunity in Pkmn's resistances, remove resistance and add immunity
                elif immunity in pkmn.resists.all():
                    pkmn.resists.remove(immunity)
                    pkmn.immune_to.add(immunity)
                #add immunity
                else:
                    pkmn.immune_to.add(immunity)

    def rating_avg(self, pkmn_id):
        pkmn = Pokemon.objects.get(id = pkmn_id)
        total = 0
        for review in pkmn.reviews.all():
            total += review.rating
        avg = total/len(pkmn.reviews.all())
        return round(avg, 2)

    def get_total(self, index):
        pkmn = Pokemon.objects.get(id = index)
        total = 0
        total += pkmn.hp
        total += pkmn.attack
        total += pkmn.defense
        total += pkmn.sp_attack
        total += pkmn.sp_defense
        total += pkmn.speed
        return total

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

class ReviewManager(models.Manager):
    def new_review(self, postData, user, pkmn):
        if len(postData['review']) < 1 or len(postData['review']) > 255:
            return None
        else:
            return Review.objects.create(
                content = postData['review'],
                rating = postData['rating'],
                added_by = user,
                pkmn = pkmn
            )

class Pokemon(models.Model):
    name = models.CharField(max_length=200, null = True)
    gen = models.IntegerField(null = True)
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

    def __str__(self):
        return f"{self.id} {self.name.capitalize()}"

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
    objects = ReviewManager()