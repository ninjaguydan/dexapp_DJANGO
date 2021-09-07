from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import re
import bcrypt

# Model validators
class UserManager(BaseUserManager):
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

    def update_user(self, user, postData, fileData):
        user.first_name = postData['fname']
        user.last_name = postData['lname']
        user.bg_color = postData['color']
        #if current user image is a default image
        if "default" in user.user_img.url:
            #check if an image was uploaded, and replace if true
            if "img-uploaded" in fileData:
                user.user_img = fileData['img-uploaded']
            #otherwise user image becomes new default image
            else:
                user.user_img = postData['img']
        #if current user image is an uploaded image
        else:
            #check if a new image was uploaded and replace if so
            if "img-uploaded" in fileData:
                user.user_img.delete()
                user.user_img = fileData['img-uploaded']
            #if a new image was not uploaded but no new image was selected, keep it the same
            elif "images" in postData['img']:
                print('We kept the same image!')
            #replace with new selected image
            else:
                user.user_img.delete()
                user.user_img = postData['img']         
        user.save()

    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0]
        return user.check_password(password)

    def create_user(self, first_name, last_name, email, username, password):
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def register(self, form):
        # pw = bcrypt.hashpw(form['pw'].encode(), bcrypt.gensalt()).decode()
        return self.create_user(
            first_name = form['fname'],
            last_name = form['lname'],
            username = form['username'],
            email = (form['email']),
            password = form['pw']
        )

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

    def get_timeline(self, user):
        timeline = {}
        for post in user.posts.all():
            timeline[post.created_at] = post
        for review in user.reviews_added.all():
            timeline[review.created_at] = review
        for team in user.teams.all():
            timeline[team.created_at] = team
        following = user.profile.following.all()
        for person in following:
            for post in person.posts.all():
                timeline[post.created_at] = post
            for review in person.reviews_added.all():
                timeline[review.created_at] = review
            for team in person.teams.all():
                timeline[team.created_at] = team
        return timeline

    def guest_timeline(self):
        timeline = {}
        for user in User.objects.all():
            for post in user.posts.all():
                timeline[post.created_at] = post
            for review in user.reviews_added.all():
                timeline[review.created_at] = review
            for team in user.teams.all():
                timeline[team.created_at] = team
        return timeline

class User(AbstractBaseUser):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 30, unique = True)
    email = models.EmailField(verbose_name = "email", max_length = 50, unique = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    user_img = models.ImageField(default = "/default/0.png", upload_to="images/", validators = [FileExtensionValidator(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])])
    bg_color = models.CharField(max_length = 20, default = "gray")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    objects = UserManager()