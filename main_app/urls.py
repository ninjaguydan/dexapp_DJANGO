from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pkmn_id>', views.pokemon),
    path('team/<int:team_id>', views.display_team),
    path('<int:team_id>/comment_team', views.comment_team),
    path('<int:comment_id>/delete_team_comment', views.delete_team_comment),
    path('like_team_comment', views.like_team_comment),
    path('favorite', views.favorite),
    path('<int:pkmn_id>/create_review', views.create_review),
    path('<int:review_id>/delete_review', views.delete_review),
    path('like_review', views.like_review),
    path('<int:review_id>/comment_review', views.comment_review),
    path('<int:comment_id>/delete_review_comment', views.delete_review_comment),
    path('like_review_comment', views.like_review_comment),
    path('<int:pkmn_id>/create_team', views.create_team),
    path('<int:team_id>/update_team', views.update_team),
    path('<int:pkmn_id>/add_to_team', views.add_to_team),
    path('like_team', views.like_team),
    path('<int:team_id>/delete_team', views.delete_team),
]