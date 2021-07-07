from django.shortcuts import render, redirect
from django.db.models import Count
from main_app.models import *
import random
import requests
import json

# Create your views here.

def index(request):
    if len(Pokemon.objects.all()) == 0:
        for i in range(1,899):
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}/")
            Pokemon.objects.create(
                name = response.json()["name"],
                sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png",
                shiny_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{i}.png",
                art_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{i}.png",
                height = response.json()["height"],
                weight = response.json()["weight"],
            )
        return redirect('/')
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    context = {
        "user" : user,
        "statuses" : Status.objects.all().order_by("created_at")[:5],
        "reviews" : Review.objects.all().order_by("created_at")[:10],
        "all_pokemon" : Pokemon.objects.annotate(count = Count('favorited_by')).order_by('-count')[:30],
    }
    return render(request, "index.html", context)

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
        prev = pkmn_id-1
    else:
        prev = 898
    #look at next pokemon object and grab sprite url if it exits
    if pkmn_id+1 != 899:
        nxt = pkmn_id+1
    else:
        nxt = 1
    context = {
        "pokemon" : pokemon,
        "user" : user,
        "average" : round(avg, 2),
        "prev" : f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{prev}.png",
        "prev_num" : prev,
        "next" : f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{nxt}.png",
        "next_num" : nxt,
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

def add_pkmn(request, pkmn_id):
    user = User.objects.get(id = request.session['userid'])
    pkmn = Pokemon.objects.get(id = pkmn_id)
    if len(user.team.all()) < 6:
        user.team.add(pkmn)
    return redirect(f'/pkmn/{pkmn_id}')

def remove_pkmn(request, pkmn_id):
    user = User.objects.get(id = request.session['userid'])
    pkmn = Pokemon.objects.get(id = pkmn_id)
    user.team.remove(pkmn)
    return redirect(f'/pkmn/{pkmn_id}')

def profile(request, profile_id):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    context = {
        "user" : user,
        "profile" : User.objects.get(id = profile_id),
    }
    return render(request, "profile.html", context)

def post_status(request, user_id):
    if request.method == "GET":
        return redirect(f'/{user_id}')
    user = User.objects.get(id= user_id)
    Status.objects.create(
        content = request.POST['status'],
        added_by = user,
    )
    return redirect(f'/{user_id}')

def delete_status(request, status_id):
    status_to_delete = Status.objects.get(id = status_id)
    user_id = status_to_delete.added_by.id
    status_to_delete.delete()
    return redirect(f'/{user_id}')

def comment_status(request, status_id):
    status = Status.objects.get(id = status_id)
    profile = User.objects.get(id = status.added_by.id)
    user = User.objects.get(id = request.session['userid'])
    Comment.objects.create(
        content = request.POST['comment'],
        added_by = user,
        status = status
    )
    return redirect(f'/{profile.id}')

def delete_status_comment(request, comment_id):
    comment_to_delete = Comment.objects.get(id = comment_id)
    status = Status.objects.get(id = comment_to_delete.status.id)
    profile = User.objects.get(id = status.added_by.id)
    comment_to_delete.delete()
    return redirect(f'/{profile.id}')