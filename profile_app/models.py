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

    def get_stats(self, index):
        Pokemon = apps.get_model(app_label='main_app', model_name='Pokemon')
        team = Team.objects.get(id = index)
        count = len(team.pkmn.all())
        table = {}
        base_total = 0
        hp_total = 0
        atk_total = 0
        def_total = 0
        spatk_total = 0
        spdef_total = 0
        spd_total = 0
        for pkmn in team.pkmn.all():
            s_total = Pokemon.objects.get_total(pkmn.id)
            base_total += s_total
            hp_total += pkmn.hp
            atk_total += pkmn.attack
            def_total += pkmn.defense
            spatk_total += pkmn.sp_attack
            spdef_total += pkmn.sp_defense
            spd_total += pkmn.speed
        table['Base Stat Total Avg'] = round(base_total/count)
        table['Avg HP'] = round(hp_total/count)
        table['Avg Attack'] = round(atk_total/count)
        table['Avg Defense'] = round(def_total/count)
        table['Avg Special Attack'] = round(spatk_total/count)
        table['Avg Special Defense'] = round(spdef_total/count)
        table['Avg Speed'] = round(spd_total/count)
        return table

class ProfileManager(models.Manager):
    def update(self, postData, index):
        profile = Profile.objects.get(id = index)
        if len(postData['bio']) == 0 or postData['bio'] == "None":
            profile.bio = None
        else:
            profile.bio = postData['bio']
        if len(postData['location']) == 0 or postData['location'] == "None":
            profile.location = None
        else:
            profile.location = postData['location']
        if len(postData['pronouns']) == 0 or postData['pronouns'] == "None":
            profile.pronouns = None
        else:
            profile.pronouns = postData['pronouns']
        profile.save()
        return

class PostManager(models.Manager):
    def new_post(self, user, postData):
        if len(postData['post']) < 1 or len(postData['post']) > 255:
            return None
        else:
            return Post.objects.create(
                content = postData['post'],
                added_by = user,
            )

class CommentManager(models.Manager):
    def new_post_comment(self, postData, user, post):
        if len(postData['comment']) < 1 or len(postData['comment']) > 255:
            return None
        else:
            return Comment.objects.create(
                content = postData['comment'],
                added_by = user,
                post = post,
            )
    def new_team_comment(self, postData, user, team):
        if len(postData['comment']) < 1 or len(postData['comment']) > 255:
            return None
        else:
            return Comment.objects.create(
                content = postData['comment'],
                added_by = user,
                team = team,
            )
    def new_review_comment(self, postData, user, review):
        if len(postData['comment']) < 1 or len(postData['comment']) > 255:
            return None
        else:
            return Comment.objects.create(
                content = postData['comment'],
                added_by = user,
                review = review,
            )
class MessageManager(models.Manager):
    def create_message(self, postData, user, profile):
        thread = Thread.objects.filter(users__id = user.id).filter(users__id = profile.id)
        if len(thread) == 0:
            shared_thread = Thread.objects.create(user_2 = profile)
            shared_thread.users.add(user, profile)
        else:
            shared_thread = thread[0]
        if len(postData['message']) > 0 and len(postData['message']) < 255:
            return Message.objects.create(
                content = postData['message'],
                sender = user,
                receiver = profile,
                thread = shared_thread,
            )
        else:
            return None

class Profile(models.Model):
    user = models.OneToOneField(User, related_name = "profile", on_delete=models.CASCADE)
    bio = models.TextField(null = True)
    location = models.CharField(max_length=100, null = True)
    pronouns = models.CharField(max_length=20, null = True)
    following = models.ManyToManyField(User, related_name = "following", blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProfileManager()

class Post(models.Model):
    content = models.TextField()
    added_by = models.ForeignKey(User, related_name = "posts", null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "liked_posts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PostManager()

class Thread(models.Model):
    users = models.ManyToManyField(User, related_name = "threads")
    user_2 = models.ForeignKey(User, on_delete = models.CASCADE, null = True) #delete null later
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, related_name = "messages_sent", on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name = "messages", on_delete = models.CASCADE)
    thread = models.ForeignKey(Thread, related_name = "messages", on_delete = models.CASCADE, null = True) #delete null later
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

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
    objects = CommentManager()