from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from profile_app.models import Profile

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


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

def password_reset_request(request):
    if request.method == "POST":
        pw_form = PasswordResetForm(request.POST)
        if pw_form.is_valid():
            data = pw_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = "Password Reset Request"
                    email_template_name = 'password_message.txt'
                    parameters = {
                        'email' : user.email,
                        'domain' : 'localhost:8000',
                        'site_name' : 'DexApp',
                        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                        'token' : default_token_generator.make_token(user),
                        'protocol' : 'http',
                        'username' : user.first_name.capitalize(),
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
    else:
        pw_form = PasswordResetForm()

    context = {
        "password_form" : pw_form,
    }
    return render(request, "pw_reset.html", context)