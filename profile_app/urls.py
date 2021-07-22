from django.urls import path
from . import views

urlpatterns = [
    path('<int:profile_id>', views.profile),
    path('<int:user_id>/update', views.update_profile),
    path('follow', views.follow),
    path('<int:user_id>/post_post', views.post_post),
    path('<int:post_id>/delete_post', views.delete_post),
    path('<int:post_id>/like_post', views.like_post),
    path('<int:post_id>/unlike_post', views.unlike_post),
    path('<int:post_id>/comment_post', views.comment_post),
    path('<int:comment_id>/delete_post_comment', views.delete_post_comment),
    path('<int:comment_id>/like_post_comment', views.like_post_comment),
    path('<int:comment_id>/unlike_post_comment', views.unlike_post_comment),
]