from profile_app.models import Post
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
# from django.apps import apps
# User = apps.get_model("login_app", "User")

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=200, null = True)
    sprite_url = models.CharField(max_length=200, null = True)
    shiny_url = models.CharField(max_length=200, null = True)
    art_url = models.CharField(max_length=200, null = True)
    height = models.IntegerField(null = True)
    weight = models.IntegerField(null = True)
    favorited_by = models.ManyToManyField(User, related_name = "favorites")
    teams = models.ManyToManyField(User, related_name = "team")

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    added_by = models.ForeignKey(User, related_name = "reviews_added", null = True, on_delete = models.CASCADE)
    pkmn = models.ForeignKey(Pokemon, related_name = "reviews", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
