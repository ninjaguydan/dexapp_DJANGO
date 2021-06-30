from django.db import models
from login_app.models import *

# Create your models here.
class Pokemon(models.Model):
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