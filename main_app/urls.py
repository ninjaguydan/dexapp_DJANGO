from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('pkmn/<int:pkmn_id>', views.pokemon),
    path('pkmn/<int:pkmn_id>/fav', views.favorite),
    path('pkmn/<int:pkmn_id>/unfav', views.unfavorite),
    path('pkmn/<int:pkmn_id>/post_review', views.post_review),
    path('pkmn/<int:pkmn_id>/add_pkmn', views.add_pkmn),
    path('pkmn/<int:pkmn_id>/remove_pkmn', views.remove_pkmn),
    path('pkmn/<int:review_id>/delete_review', views.delete_review),
    path('<int:profile_id>', views.profile),
    path('<int:user_id>/post_status', views.post_status),
    path('<int:status_id>/delete_status', views.delete_status),
]