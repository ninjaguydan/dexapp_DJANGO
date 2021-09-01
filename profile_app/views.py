from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post, Message, Comment, Profile
from login_app.models import User


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

def update_profile(request, user_id):
    if request.method == "GET":
        return redirect(f'/profile/{user_id}')
    errors = User.objects.update_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/profile/{user_id}')
    user = User.objects.get(id = user_id)
    User.objects.update_user(user, request.POST, request.FILES)
    Profile.objects.update(request.POST, user_id)
    return redirect(f'/profile/{user_id}')

def delete_profile(request):
    #Check if anyone is logged in
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
        request.session.clear()
        user.delete()
        return redirect('/login/register')
    return redirect('/')

def follow(request):
    if request.method == "GET":
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['userid'])
        user_to_follow = User.objects.get(id = request.POST['follow'])
        if user_to_follow in user.profile.following.all():
            user.profile.following.remove(user_to_follow)
        else:
            user.profile.following.add(user_to_follow)
        return redirect(f'/profile/{user_to_follow.id}')

def create_post(request, user_id):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id= user_id)
    post = Post.objects.new_post(user, request.POST)
    if request.META.get('HTTP_REFERER')[-1] == "/":
        return redirect('/')
    else:
        # print(f"We got here from {request.META.get('HTTP_REFERER')}!!")
        context = {"user" : user, "post" : post, "profile" : user}
        return render(request, "post.html", context)

def delete_post(request, post_id):
    #check if anyone is logged in
    if "userid" in request.session:
        post_to_delete = Post.objects.get(id = post_id)
        #delete post if logged in user is also post's author
        if request.session['userid'] == post_to_delete.added_by.id:
            post_to_delete.delete()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

def like_post(request):
    #if GET request, redirect 
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    post = Post.objects.get(id = request.POST['like'])
    #if user already likes post, unlike post
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    context = {"user" : user, "post" : post}
    return render(request, "post-like.html", context)

def comment_post(request, post_id):
    if request.method == "GET":
        return redirect(request.META.get('HTTP_REFERER'))
    post = Post.objects.get(id = post_id)
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.new_post_comment(request.POST, user, post)
    context = {"post" : post, "comment" : comment, "user" : user}
    return render(request, "post-comment.html", context)

def delete_post_comment(request, comment_id):
    #check if anyone is logged in
    if "userid" in request.session:
        comment_to_delete = Comment.objects.get(id = comment_id)
        #delete comment if logged in user is also comment's author
        if request.session['userid'] == comment_to_delete.added_by.id:
            comment_to_delete.delete()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

def like_post_comment(request):
    #if GET request, redirect
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.get(id = request.POST['like'])
    #if user already likes post comment, unlike post comment
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
    #otherwise, like post comment
        comment.likes.add(user)
    context = {"comment" : comment, "user" : user}
    return render(request, "post-comment-like.html", context)

def messages(request):
    if "userid" in request.session:
        user = User.objects.get(id = request.session['userid'])
    else:
        return redirect("/")
    messages = Message.objects.all()
    context = {"user" : user, "messages" : messages}
    return render(request, "messages.html", context)

def send_message(request, profile_id):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    recipient = User.objects.get(id = profile_id)
    message = Message.objects.create(
        content = request.POST['message'],
        user = user,
        receiver = recipient
    )
    if "messages" in request.META.get('HTTP_REFERER'):
        context = {"user" : user, "message" : message}
    else:
        return redirect(request.META.get('HTTP_REFERER'))