from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pkmn_id>', views.pokemon),
    path('favorite', views.favorite),
    path('<int:pkmn_id>/create_review', views.create_review),
    path('<int:review_id>/delete_review', views.delete_review),
    path('like_review', views.like_review),
    path('<int:review_id>/comment_review', views.comment_review),
    path('<int:comment_id>/delete_review_comment', views.delete_review_comment),
    path('like_review_comment', views.like_review_comment),
]