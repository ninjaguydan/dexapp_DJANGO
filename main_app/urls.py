from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('pkmn/<int:pkmn_id>', views.pokemon),
    path('pkmn/<int:pkmn_id>/fav', views.favorite),
]