# Generated by Django 2.2 on 2021-09-04 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
        ('profile_app', '0004_auto_20210904_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='new_followers',
            field=models.ManyToManyField(related_name='new', to='login_app.User'),
        ),
        migrations.AddField(
            model_name='profile',
            name='notif_counter',
            field=models.IntegerField(default=0),
        ),
    ]