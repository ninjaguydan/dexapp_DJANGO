from django.core import paginator
from django.shortcuts import render, redirect
from login_app.models import User
from main_app.models import Pokemon, Type
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def search(request):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    query = request.GET['q']
    if request.GET['filter'] == "people":
        results = User.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query) | Q(username__contains = query)).order_by('username')
    else:
        results = Pokemon.objects.filter(name__contains = query).order_by('name')
    #pagination/ Infinite scroll
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 24)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {
        "query" : query, 
        "result" : request.GET['filter'], 
        "user" : user, 
        "count" : paginator.count, 
        "page" : page,}
    return render(request, "results.html", context)

def dex(request):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    pokemon = Pokemon.objects.all()
    gen = "all"
    pkmn_type = "all"
    if "gen" in request.GET:
        if request.GET['gen'] != "all" and request.GET['type'] != "all":
            pokemon = pokemon.filter(
                gen = request.GET['gen'],
                types__id = request.GET['type'], 
                )
            gen = request.GET['gen']
            pkmn_type = request.GET['type']
        elif request.GET['gen'] != "all":
            pokemon = pokemon.filter(gen = request.GET['gen'])
            gen = request.GET['gen']
        elif request.GET['type'] != "all":
            pokemon = pokemon.filter(types__id = request.GET['type'])
            pkmn_type = request.GET['type']

    #pagination/infinite scroll
    page = request.GET.get('page', 1)
    paginator = Paginator(pokemon, 24)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {
        "user" : user,
        "pokemon" : page,
        "types" : Type.objects.all().order_by('name'),
        "gen" : gen,
        "type" : pkmn_type,

        }
    return render(request, "pokedex.html", context)