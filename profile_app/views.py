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
        return redirect(f'/{user_id}')
    errors = User.objects.update_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{user_id}')
    user = User.objects.get(id = user_id)
    profile = Profile.objects.get(id = user.profile.id)
    user.first_name = request.POST['fname']
    user.last_name = request.POST['lname']
    profile.bio = request.POST['bio']
    user.default_img = request.POST['img']
    user.bg_color = request.POST['color']
    user.save()
    profile.save()
    return redirect(f'/profile/{user_id}')

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
    Post.objects.create(
        content = request.POST['post'],
        added_by = user,
    )
    print(f"We got here from {request.META.get('HTTP_REFERER')}!!")
    #redirect to the page we came from
    return redirect(request.META.get('HTTP_REFERER'))

def delete_post(request, post_id):
    post_to_delete = Post.objects.get(id = post_id)
    user_id = post_to_delete.added_by.id
    #post can only be deleted by author
    if request.session['userid'] != user_id:
        return redirect('/')
    post_to_delete.delete()
    #redirect to the page we came from
    return redirect(request.META.get('HTTP_REFERER'))

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
    #redirect to the page we came from
    return redirect(request.META.get('HTTP_REFERER'))

def comment_post(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.method == "GET":
        return redirect(f'/profile/{post.added_by.id}')
    user = User.objects.get(id = request.session['userid'])
    Comment.objects.create(
        content = request.POST['comment'],
        added_by = user,
        post = post
    )
    return redirect(f'/profile/{post.added_by.id}')

def delete_post_comment(request, comment_id):
    comment_to_delete = Comment.objects.get(id = comment_id)
    #comment can only be deleted by author
    if request.session['userid'] != comment_to_delete.added_by.id:
        return redirect('/')
    post = Post.objects.get(id = comment_to_delete.post.id)
    comment_to_delete.delete()
    return redirect(f'/profile/{post.added_by.id}')

def like_post_comment(request, comment_id):
    #if GET request, redirect
    #if user already likes post comment, unlike post comment
    #otherwise, like post comment
    pass