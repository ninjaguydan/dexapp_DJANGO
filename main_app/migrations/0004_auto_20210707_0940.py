# Generated by Django 2.2 on 2021-07-07 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
        ('main_app', '0003_auto_20210706_2337'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]