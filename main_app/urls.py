from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pkmn_id>', views.pokemon),
    path('<int:pkmn_id>/fav', views.favorite),
    path('<int:pkmn_id>/create_review', views.create_review),
    path('<int:review_id>/delete_review', views.delete_review),
    path('<int:review_id>/like_review', views.like_review),
    path('<int:review_id>/comment_review', views.comment_review),
    path('<int:comment_id>/delete_review_comment', views.delete_review_comment),
    path('<int:comment_id>/like_review_comment', views.like_review_comment),
]