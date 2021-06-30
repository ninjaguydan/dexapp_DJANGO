from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.

#render login page
def login(request):
    return render(request, "login.html")

#log in the user
def user_login(request):
    #only allow access to this method via POST request
    if request.method == "GET":
        return redirect('/login')
    #use our 'authenticate' method to check for User
    if not User.objects.authenticate(request.POST['email'], request.POST['pw']):
        messages.error(request, "Email or password does not match our records")
        return redirect('/login')
    #get User and add them to session
    user = User.objects.get(email= request.POST['email'])
    request.session['userid'] = user.id
    return redirect("/")

#render registration poage
def register(request):
    return render(request, "register.html")

#add new user to database
def signup(request):
    #only allow access to this method via POST request
    if request.method == "GET":
        return redirect('/login/register')
    #assign the dictionary returned from our 'validator' method to a variable
    errors = User.objects.validator(request.POST)
    #if anything exists in the dict, add them to 'messages' to display on front end...
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login/register')
    # ...Otherwise, create new user with 'register' method
    else:
        new_user = User.objects.register(request.POST)
        request.session['userid'] = new_user.id
        return redirect("/")