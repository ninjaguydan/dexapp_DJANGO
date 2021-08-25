from django.shortcuts import render, redirect
from django.db.models import Count
from login_app.models import User
from .models import Review, Pokemon, Type
from profile_app.models import Post, Comment, Team
import collections
import requests
import json

def index(request):
    # Initialize Pokemon, Types, and type relationships
    if len(Type.objects.all()) == 0:
        # Create table for all 18 types
        for i in range(1,19):
            Type.objects.create_type(i)
        # Create Type relationships
        for t in Type.objects.all():
            Type.objects.add_relation(t.id)
        return redirect('/')
    # Create table for all 898 Pokemon
    if len(Pokemon.objects.all()) == 0:
        for i in range(1,899):
            Pokemon.objects.create_pkmn(i)
            #add types to pokemon
            Pokemon.objects.add_types(i)
            #add weakness/resistance info to pokemon
            Pokemon.objects.add_weaknesses(i)
            #add gen
            Pokemon.objects.add_gen(i)
        return redirect('/')
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    #get all posts, reviews, and teams from people the User follows
    #and order them chronologically
    timeline = User.objects.get_timeline(user)
    ordered_tl = collections.OrderedDict(sorted(timeline.items()))
    context = {
        "user" : user,
        "timeline" : ordered_tl,
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
    if pokemon.reviews.all():
        avg = Pokemon.objects.rating_avg(pkmn_id)
    else:
        avg = 0
    #if pokemon ID is 1, the previous ID becomes 898
    if pkmn_id-1 != 0:
        prev = pkmn_id-1
    else:
        prev = 898
    #if pokemon ID is 898, the next ID becomes 1
    if pkmn_id+1 != 899:
        nxt = pkmn_id+1
    else:
        nxt = 1
    context = {
        "pokemon" : pokemon,
        "user" : user,
        "average" : avg,
        "prev" : f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{prev}.png",
        "prev_num" : prev,
        "next" : f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{nxt}.png",
        "next_num" : nxt,
        "total" : Pokemon.objects.get_total(pkmn_id),
    }
    return render(request, "pokemon.html", context)

def display_team(request, team_id):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        user = None
    context = {
        "r_table" : Team.objects.get_resistance(team_id),
        "s_table" : Team.objects.get_stats(team_id),
        "user" : user,
        "team" : Team.objects.get(id = team_id),
    }
    return render(request, "team.html", context)

def comment_team(request, team_id):
    if request.method == "GET":
        return redirect(request.META.get('HTTP_REFERER'))
    team = Team.objects.get(id = team_id)
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.new_team_comment(request.POST, user, team)
    context = {"user" : user, "team" : team, "comment" : comment}
    return render(request, "team-comment.html", context)

def delete_team_comment(request, comment_id):
    if "userid" in request.session:
        comment_to_delete = Comment.objects.get(id = comment_id)
        if request.session['userid'] == comment_to_delete.added_by.id:
            comment_to_delete.delete()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

def like_team_comment(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.get(id = request.POST['like'])
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    context = {"user" : user, "comment" : comment}
    return render(request,"team-comment-like.html",context)

def favorite(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    pokemon = Pokemon.objects.get(id = request.POST['pokemon'])
    if pokemon in user.favorites.all():
        user.favorites.remove(pokemon)
    else:
        user.favorites.add(pokemon)
    return redirect(request.META.get('HTTP_REFERER'))

def create_review(request, pkmn_id):
    if request.method == "GET":
        return redirect(f'pkmn/{pkmn_id}')
    pkmn = Pokemon.objects.get(id = pkmn_id)
    user = User.objects.get(id=request.session['userid'])
    review = Review.objects.new_review(request.POST, user, pkmn)
    context = {"pokemon": pkmn, "user" : user, "review" : review}
    return render(request, "pokemon-review.html", context)

def delete_review(request, review_id):
    #Check if user is logged in
    if "userid" in request.session:
        review_to_delete = Review.objects.get(id = review_id)
        #Delete review if logged in user is the review's author
        if request.session['userid'] == review_to_delete.added_by.id:
            review_to_delete.delete()
            print("we came from", request.META.get('HTTP_REFERER'))
            print("the path is", request.path)
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

def like_review(request):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    review = Review.objects.get(id = request.POST['like'])
    #if user in review's likes, remove them
    if user in review.likes.all():
        review.likes.remove(user)
    else:
    #otherwise, add them
        review.likes.add(user)
    context = {"user" : user, "review" : review}
    return render(request, "review-likes-partial.html", context)

def comment_review(request, review_id):
    if request.method == "GET":
        return redirect('/')
    review = Review.objects.get(id = review_id)
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.new_review_comment(request.POST, user, review)
    context = {"review" : review, "user" : user, "comment" : comment}
    return render(request, "review-comment-partial.html", context)

def delete_review_comment(request, comment_id):
    #Check if user is logged in
    if "userid" in request.session:
        comment_to_delete = Comment.objects.get(id = comment_id)
        #Delete comment if logged in user is the comment's author
        if request.session['userid'] == comment_to_delete.added_by.id:
            comment_to_delete.delete()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

def like_review_comment(request):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.get(id = request.POST['like'])
    #if user in review comment's likes, remove them
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
    #otherwise, like post comment
        comment.likes.add(user)
    context = {"user" : user, "comment" : comment}
    return render(request, "review-comment-likes-partial.html", context)
    # return redirect(request.META.get('HTTP_REFERER'))

def create_team(request, pkmn_id):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    pkmn = Pokemon.objects.get(id = pkmn_id)
    new_team = Team.objects.create(
        name = request.POST['name'],
        user = user
    )
    new_team.pkmn.add(pkmn)
    #post update to team page
    update = Comment.objects.create(
        content = "added!",
        team = new_team
    )
    update.pkmn.add(pkmn)
    context = {"team" : new_team}
    return render(request, "pokemon-team.html", context)

def update_team(request, team_id):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    team = Team.objects.get(id = team_id)
    team.name = request.POST['name']
    #get all selected pokemon as a list[]
    pokemon = request.POST.getlist('pkmn')
    for i in pokemon:
        pkmn = Pokemon.objects.get(id = i)
        team.pkmn.remove(pkmn)
        #post update to team page
        update = Comment.objects.create(
            content = "removed!",
            team = team,
        )
        update.pkmn.add(pkmn)
    return redirect(request.META.get('HTTP_REFERER'))

def add_to_team(request, pkmn_id):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    pkmn = Pokemon.objects.get(id = pkmn_id)
    #get all selected teams as a list[]
    teams = request.POST.getlist('teams')
    teams_added = []
    for i in teams:
        #add pokemon to each selected team in the list[]
        team = Team.objects.get(id = i)
        #if team has 6 pokemon, dont let them add
        if len(team.pkmn.all()) == 6:
            print(f'{pkmn.name} was not added to {team.name}')
            return redirect(request.META.get('HTTP_REFERER'))
        team.pkmn.add(pkmn)
        #post update to team page
        update = Comment.objects.create(
            content = "added!",
            team = team,
        )
        update.pkmn.add(pkmn)
        teams_added.append(team)
    context = {
        "teams_added" : teams_added 
    }
    return render(request, "pokemon-success.html", context)

def like_team(request):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    team = Team.objects.get(id = request.POST['like'])
    if user in team.likes.all():
    #if user in team's likes, remove them
        team.likes.remove(user)
    else:
    #otherwise, add them
        team.likes.add(user)
    if request.META.get('HTTP_REFERER') != None and "/team/" in request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        context = {"user" : user, "team" : team}
        print(request.META.get('HTTP_REFERER'))
        return render(request,"team-like.html", context)

def delete_team(request, team_id):
    #Check if anyone is logged in
    if "userid" in request.session:
        team_to_delete = Team.objects.get(id = team_id)
        #Check if logged in user is the one who made the team
        if request.session['userid'] == team_to_delete.user.id:
            team_to_delete.delete()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')