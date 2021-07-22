from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('pkmn/<int:pkmn_id>', views.pokemon),
    path('pkmn/<int:pkmn_id>/fav', views.favorite),
    path('pkmn/<int:pkmn_id>/unfav', views.unfavorite),
    path('pkmn/<int:pkmn_id>/add_pkmn', views.add_pkmn),
    path('pkmn/<int:pkmn_id>/remove_pkmn', views.remove_pkmn),
    path('pkmn/<int:pkmn_id>/post_review', views.post_review),
    path('pkmn/<int:review_id>/delete_review', views.delete_review),
    path('pkmn/<int:review_id>/like_review', views.like_review),
    path('pkmn/<int:review_id>/unlike_review', views.unlike_review),
    path('pkmn/<int:review_id>/comment_review', views.comment_review),
    path('pkmn/<int:comment_id>/delete_review_comment', views.delete_review_comment),
    path('pkmn/<int:comment_id>/like_review_comment', views.like_review_comment),
    path('pkmn/<int:comment_id>/unlike_review_comment', views.unlike_review_comment),
<<<<<<< HEAD
=======
    path('<int:profile_id>', views.profile),
    path('<int:user_id>/update', views.update_profile),
    path('<int:profile_id>/follow', views.follow),
    path('<int:profile_id>/unfollow', views.unfollow),
    path('<int:user_id>/post_status', views.post_status),
    path('<int:status_id>/delete_status', views.delete_status),
    path('<int:status_id>/like_status', views.like_status),
    path('<int:status_id>/unlike_status', views.unlike_status),
    path('<int:status_id>/comment_status', views.comment_status),
    path('<int:comment_id>/delete_status_comment', views.delete_status_comment),
    path('<int:comment_id>/like_status_comment', views.like_status_comment),
    path('<int:comment_id>/unlike_status_comment', views.unlike_status_comment),
>>>>>>> parent of 1f6f66a (replaced friend functionality with follow functionality)
]