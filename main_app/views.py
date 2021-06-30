from django.shortcuts import render, redirect
from main_app.models import *
import requests
import json

# Create your views here.
def index(request):
    if len(Pokemon.objects.all()) == 0:
        for i in range(897): 
            Pokemon.objects.create()
        return redirect('/')
    else:
        if "userid" in request.session:
            context = {
                "user" : User.objects.get(id = request.session['userid']),
            }
            return render(request, "index.html", context)
        return render(request, "index.html")

def logout(request):
    request.session.clear()
    return redirect('/login')

def pokemon(request, pkmn_id):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pkmn_id}/")
    pokemon = Pokemon.objects.get(id = pkmn_id)
    context = {
        "pokemon" : pokemon,
        "name" : response.json()["name"].capitalize(),
        "img_url" : f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pkmn_id}.png",
        "height" : response.json()["height"],
        "weight" : response.json()["weight"],
    }
    return render(request, "pokemon.html", context)

def favorite(request, pkmn_id):
    pass