# Generated by Django 2.2 on 2021-09-06 19:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('user_img', models.ImageField(default='/default/0.png', upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])])),
                ('bg_color', models.CharField(default='gray', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
