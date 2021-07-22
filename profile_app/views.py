from django.shortcuts import render, redirect
from main_app.models import *
from django.contrib import messages


# Create your views here.
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
    user.first_name = request.POST['fname']
    user.last_name = request.POST['lname']
    user.bio = request.POST['bio']
    user.default_img = request.POST['img']
    user.bg_color = request.POST['color']
    user.save()
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

def post_post(request, user_id):
    if request.method == "GET":
        return redirect(f'/{user_id}')
    user = User.objects.get(id= user_id)
    Post.objects.create(
        content = request.POST['post'],
        added_by = user,
    )
    return redirect(f'/profile/{user_id}')

def delete_post(request, post_id):
    post_to_delete = Post.objects.get(id = post_id)
    user_id = post_to_delete.added_by.id
    post_to_delete.delete()
    return redirect(f'/profile/{user_id}')

def like_post(request, post_id):
    user = User.objects.get(id = request.session['userid'])
    post = Post.objects.get(id = post_id)
    post.likes.add(user)
    return redirect(f'/profile/{post.added_by.id}')

def unlike_post(request, post_id):
    user = User.objects.get(id = request.session['userid'])
    post = Post.objects.get(id = post_id)
    post.likes.remove(user)
    return redirect(f'/profile/{post.added_by.id}')

def comment_post(request, post_id):
    post = Post.objects.get(id = post_id)
    profile = User.objects.get(id = post.added_by.id)
    user = User.objects.get(id = request.session['userid'])
    Comment.objects.create(
        content = request.POST['comment'],
        added_by = user,
        post = post
    )
    return redirect(f'/profile/{profile.id}')

def delete_post_comment(request, comment_id):
    comment_to_delete = Comment.objects.get(id = comment_id)
    post = Post.objects.get(id = comment_to_delete.post.id)
    profile = User.objects.get(id = post.added_by.id)
    comment_to_delete.delete()
    return redirect(f'/profile/{profile.id}')

def like_post_comment(request, comment_id):
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.get(id = comment_id)
    comment.likes.add(user)
    return redirect(f'/profile/{comment.post.added_by.id}')

def unlike_post_comment(request, comment_id):
    user = User.objects.get(id = request.session['userid'])
    comment = Comment.objects.get(id = comment_id)
    comment.likes.remove(user)
    return redirect(f'/profile/{comment.post.added_by.id}')