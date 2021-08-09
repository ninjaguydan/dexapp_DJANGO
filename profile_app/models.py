from django.db import models
from login_app.models import User
from django.apps import apps

class TeamManager(models.Manager):
    def get_resistance(self, index):
        Type = apps.get_model(app_label='main_app', model_name='Type')
        table = {}
        for t in Type.objects.all().order_by('name'):
            table[t.name] = [
                {"weak" : 0},
                {"resist" : 0},
                {"immune" : 0},
            ]
        team = Team.objects.get(id = index)
        for pokemon in team.pkmn.all():
            for weakness in pokemon.weak_to.all():
                table[weakness.name][0]["weak"] += 1
            for resistance in pokemon.resists.all():
                table[resistance.name][1]["resist"] += 1
            for immunity in pokemon.immune_to.all():
                table[immunity.name][2]["immune"] += 1
        return table


class Profile(models.Model):
    user = models.OneToOneField(User, related_name = "profile", on_delete=models.CASCADE)
    bio = models.TextField(null = True)
    location = models.CharField(max_length=100, null = True)
    pronouns = models.CharField(max_length=20, null = True)
    following = models.ManyToManyField(User, related_name = "following", blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Post(models.Model):
    content = models.TextField()
    added_by = models.ForeignKey(User, related_name = "posts", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_posts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "messages_sent", on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name = "messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Team(models.Model):
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User, related_name = "teams", on_delete = models.CASCADE)
    pkmn = models.ManyToManyField('main_app.Pokemon', related_name = "teams")
    likes = models.ManyToManyField(User, related_name = "liked_teams")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TeamManager()

class Comment(models.Model):
    content = models.TextField()
    added_by = models.ForeignKey(User, related_name = "comments_added", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_comments")
    post = models.ForeignKey(Post, related_name = "comments", on_delete = models.CASCADE, null = True)
    review = models.ForeignKey('main_app.Review', related_name = "comments", on_delete = models.CASCADE, null = True)
    team = models.ForeignKey(Team, related_name = "comments", on_delete = models.CASCADE, null = True)
    pkmn = models.ManyToManyField('main_app.Pokemon')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)