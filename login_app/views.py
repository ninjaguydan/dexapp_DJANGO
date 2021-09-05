from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from profile_app.models import Profile



#render login page
def login(request):
    if "userid" in request.session:
        return redirect('/')
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
    if "userid" in request.session:
        return redirect('/')
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
    # ...Otherwise, create new user and profile with custom 'register' method
    else:
        new_user = User.objects.register(request.POST)
        Profile.objects.create(user = new_user)
        request.session['userid'] = new_user.id
        #new user is automatically followed by me
        if new_user.id != 1:
            admin = User.objects.get(id = 1)
            new_user.profile.notif_counter += 1
            new_user.profile.save()
            new_user.profile.new_followers.add(admin)
            admin.profile.following.add(new_user)
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/login')