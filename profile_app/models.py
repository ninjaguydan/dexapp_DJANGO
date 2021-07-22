from main_app.models import Pokemon
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
# from django.apps import apps
# User = apps.get_model("login_app", "User")
# Review = apps.get_model("main_app", "Review")

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name = "profile", on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name = "following", blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# class Post(models.Model):
#     content = models.TextField()
#     added_by = models.ForeignKey(User, related_name = "statuses", null = True, on_delete = models.CASCADE)
#     likes = models.ManyToManyField(User, related_name = "liked_statuses")
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "messages_sent", on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name = "messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# class Comment(models.Model):
#     content = models.TextField()
#     added_by = models.ForeignKey(User, related_name = "comments_added", null = True, on_delete = models.CASCADE)
#     likes = models.ManyToManyField(User, related_name = "liked_comments")
#     post = models.ForeignKey(Post, related_name = "comments", on_delete = models.CASCADE, null = True)
#     review = models.ForeignKey(Review, related_name = "comments", on_delete = models.CASCADE, null = True)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)

class Team(models.Model):
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User, related_name = "team", on_delete = models.CASCADE)
    pkmn = models.ManyToManyField(Pokemon, related_name = "teams")
    likes = models.ManyToManyField(User, related_name = "liked_teams")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)