from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from login_app.models import *

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=200, null = True)
    sprite_url = models.CharField(max_length=200, null = True)
    shiny_url = models.CharField(max_length=200, null = True)
    art_url = models.CharField(max_length=200, null = True)
    height = models.IntegerField(null = True)
    weight = models.IntegerField(null = True)
    favorited_by = models.ManyToManyField(User, related_name = "favorites")

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    added_by = models.ForeignKey(User, related_name = "reviews_added", null = True, on_delete = models.CASCADE)
    pkmn = models.ForeignKey(Pokemon, related_name = "reviews", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comments(models.Model):
    content = models.TextField()
    added_by = models.ForeignKey(User, related_name = "comments_added", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Status(models.Model):
    content = models.TextField()
    added_by = models.ForeignKey(User, related_name = "statuses", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_statuses")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Team(models.Model):
    user = ForeignKey(User, related_name = "team", on_delete = models.CASCADE)
    pkmn = ManyToManyField(Pokemon, related_name = "teams")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)