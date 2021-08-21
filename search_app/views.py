from django.shortcuts import render, redirect
from login_app.models import User
from main_app.models import Pokemon
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def search(request):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    query = request.GET['q']
    pokemon = Pokemon.objects.filter(name__contains = query)
    people = User.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query) | Q(username__contains = query))
    results = [*pokemon, *people]

    results_paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page = results_paginator.get_page(page_number)
    
    context = {"query" : query, "user" : user, "page" : page, "count" : results_paginator.count}
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
    pkmn_paginator = Paginator(pokemon, 24)
    page_number = request.GET.get('page')
    page = pkmn_paginator.get_page(page_number)
    context = {"query" : query, "user" : user, "page" : page}
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

    results_paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page = results_paginator.get_page(page_number)

    context = {"query" : query, "user" : user, "page" : page}
    return render(request, "results-all.html", context)