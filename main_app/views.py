from django.shortcuts import render, redirect
from django.db.models import Count
from login_app.models import User
from .models import Review, Pokemon
from profile_app.models import Post, Comment
import requests
import json

def index(request):
    #Create object for all 898 Pokemon
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
        "posts" : Post.objects.all().order_by("created_at"),
        "reviews" : Review.objects.all().order_by("created_at")[:10],
        "all_pokemon" : Pokemon.objects.annotate(count = Count('favorited_by')).order_by('-count')[:10],
    }
    return render(request, "index.html", context)

def pokemon(request, pkmn_id):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
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

def favorite(request):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    pokemon = Pokemon.objects.get(id = request.POST['pokemon'])
    #if pokemon in user's favorites, remove them
    if pokemon in user.favorites.all():
        user.favorites.remove(pokemon)
    #otherwise, add them
    else:
        user.favorites.add(pokemon)
    #redirect to the page we came from
    return redirect(request.META.get('HTTP_REFERER'))

def create_review(request, pkmn_id):
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
    return redirect(f'/{pkmn_id}')

def delete_review(request, review_id):
    review_to_delete = Review.objects.get(id = review_id)
    pkmn_id = review_to_delete.pkmn.id
    review_to_delete.delete()
    return redirect(f'/{pkmn_id}')

def like_review(request):
    #if GET request, redirect
    #if user in review's likes, remove them
    #otherwise, add them
    pass

def comment_review(request, review_id):
    review = Review.objects.get(id = review_id)
    pkmn = Pokemon.objects.get(id = review.pkmn.id)
    user = User.objects.get(id = request.session['userid'])
    Comment.objects.create(
        content = request.POST['comment'],
        added_by = user,
        review = review
    )
    return redirect(f'/{pkmn.id}')

def delete_review_comment(request, comment_id):
    comment_to_delete = Comment.objects.get(id = comment_id)
    pkmn = Pokemon.objects.get(id = comment_to_delete.review.pkmn.id)
    comment_to_delete.delete()
    return redirect(f'/{pkmn.id}')

def like_review_comment(request):
    #if GET request, redirect
    #if user in review comment's likes, remove them
    #otherwise, add them
    pass

def create_team(request):
    pass

def add_to_team(request):
    pass

def like_team(request):
    pass

def delete_team(request):
    pass