from django.db import models
import re
import bcrypt

# Model validators
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if len(postData['username']) < 6:
            errors['username'] = "Username must be at least 6 characters"
        if User.objects.filter(username = postData['username']):
            errors['username'] = "Username is already in use"
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address"
        if User.objects.filter(email = postData['email']):
            errors['email'] = f"{postData['email']} is already in use"
        if len(postData['pw']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['pw'] != postData['confirm']:
            errors['password'] = "Passwords do not match"
        return errors

    def update_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        return errors

    def update_user(self, user, postData):
        user = user
        user.first_name = postData['fname']
        user.last_name = postData['lname']
        user.default_img = postData['img']
        user.bg_color = postData['color']
        user.save()

    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['pw'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['fname'],
            last_name = form['lname'],
            username = form['username'],
            email = form['email'],
            password = pw,
        )

    def get_timeline(self, user):
        timeline = []
        for post in user.posts.all():
            timeline.append(post)
        for review in user.reviews_added.all():
            timeline.append(review)
        for team in user.teams.all():
            timeline.append(team)
        following = user.profile.following.all()
        for person in following:
            for post in person.posts.all():
                timeline.append(post)
            for review in person.reviews_added.all():
                timeline.append(review)
            for team in person.teams.all():
                timeline.append(team)
        return timeline

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 60)
    default_img = models.CharField(max_length = 2, default = 0)
    bg_color = models.CharField(max_length = 20, default = "gray")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()