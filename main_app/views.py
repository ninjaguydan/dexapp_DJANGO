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
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    # get pokemon object from api
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pkmn_id}/")
    pokemon = Pokemon.objects.get(id = pkmn_id)
    #get average of all review ratings..
    all_reviews = pokemon.reviews.all()
    if all_reviews:
        total = 0
        for review in all_reviews:
            total += review.rating
        avg = total/len(all_reviews)
    else:
        avg = 0
    #look at previous pokemon object and grab sprite url if it exits
    if pkmn_id-1 != 0:
        prev = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pkmn_id-1}.png"
    else:
        prev = None
    #look at next pokemon object and grab sprite url if it exits
    if pkmn_id+1 != 898:
        nxt = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pkmn_id+1}.png"
    else:
        nxt = None
    
    context = {
        "pokemon" : pokemon,
        "name" : response.json()["name"].capitalize(),
        "img_url" : f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pkmn_id}.png",
        "height" : response.json()["height"],
        "weight" : response.json()["weight"],
        "user" : user,
        "average" : round(avg, 2),
        "prev" : prev,
        "next" : nxt
    }
    return render(request, "pokemon.html", context)

def favorite(request, pkmn_id):
    user = User.objects.get(id=request.session['userid'])
    pkmn = Pokemon.objects.get(id=pkmn_id)
    user.favorites.add(pkmn)
    return redirect(f'/pkmn/{pkmn_id}')

def unfavorite(request, pkmn_id):
    user = User.objects.get(id=request.session['userid'])
    pkmn = Pokemon.objects.get(id=pkmn_id)
    user.favorites.remove(pkmn)
    return redirect(f'/pkmn/{pkmn_id}')

def post_review(request, pkmn_id):
    if request.method == "GET":
        return redirect(f'pkmn/{pkmn_id}')
    pkmn = Pokemon.objects.get(id = pkmn_id)
    user = User.objects.get(id=request.session['userid'])
    Review.objects.create(
        content = request.POST['review'],
        rating = request.POST['rating'],
        added_by = user,
        pkmn = pkmn
    )
    return redirect(f'/pkmn/{pkmn_id}')

def delete_review(request, review_id):
    review_to_delete = Review.objects.get(id = review_id)
    pkmn_id = review_to_delete.pkmn.id
    review_to_delete.delete()
    return redirect(f'/pkmn/{pkmn_id}')

    