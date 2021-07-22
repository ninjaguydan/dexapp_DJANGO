from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('user_login', views.user_login),
    path('register', views.register),
    path('signup', views.signup),
    path('logout', views.logout),
]