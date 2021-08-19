from django.shortcuts import render, redirect
from login_app.models import User
from main_app.models import Review, Pokemon
from django.db.models import Q
from profile_app.models import Post, Comment, Team

# Create your views here.
def search(request):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    if request.method == "GET":
        return redirect(request.META.get('HTTP_REFERER'))
    query = request.POST['q']
    pokemon = Pokemon.objects.filter(name__contains = query)
    people = User.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query) | Q(username__contains = query))
    results = [*pokemon, *people]
    context = {"query" : query, "user" : user, "results" : results}
    return render(request, "results.html", context)

def search_people(request, query):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    people = User.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query) | Q(username__contains = query))
    context = {"user" : user, "people" : people}
    return render(request, "results-people.html", context)

def search_pokemon(request, query):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    pokemon = Pokemon.objects.filter(name__contains = query)
    context = {"user" : user, "pokemon" : pokemon}
    return render(request, "results-pokemon.html", context)

# find a way to refactor all this duplicate code below
def search_all(request, query):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    pokemon = Pokemon.objects.filter(name__contains = query)
    people = User.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query) | Q(username__contains = query))
    results = [*pokemon, *people]
    context = {"query" : query, "user" : user, "results" : results}
    return render(request, "results-all.html", context)