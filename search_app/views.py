from django.core import paginator
from django.shortcuts import render, redirect
from login_app.models import User
from main_app.models import Pokemon
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def search(request):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    query = request.GET['q']
    pokemon = Pokemon.objects.filter(name__contains = query).order_by('name')
    people = User.objects.filter(Q(first_name__contains = query) | Q(last_name__contains = query) | Q(username__contains = query)).order_by('username')
    results = [*pokemon, *people,]
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 24)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {"query" : query, "user" : user, "count" : paginator.count, "page" : page,}
    return render(request, "results.html", context)