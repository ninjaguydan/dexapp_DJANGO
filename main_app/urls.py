from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('pkmn/<int:pkmn_id>', views.pokemon),
    path('pkmn/<int:pkmn_id>/fav', views.favorite),
    path('pkmn/<int:pkmn_id>/unfav', views.unfavorite),
    path('pkmn/<int:pkmn_id>/post_review', views.post_review),
    path('pkmn/<int:review_id>/delete_review', views.delete_review),
]