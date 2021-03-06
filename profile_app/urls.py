from django.urls import path
from . import views

urlpatterns = [
    path('<int:profile_id>', views.profile),
    path('<int:user_id>/update', views.update_profile),
    path('delete_profile', views.delete_profile),
    
    path('follow', views.follow),
    
    path('<int:user_id>/create_post', views.create_post),
    path('<int:post_id>/delete_post', views.delete_post),
    path('like_post', views.like_post),
    path('<int:post_id>/comment_post', views.comment_post),
    path('<int:comment_id>/delete_post_comment', views.delete_post_comment),
    path('like_post_comment', views.like_post_comment),
    
    path('messages', views.messages),
    path('messages/<int:thread_id>', views.display_thread),
    path('<int:profile_id>/send_message', views.send_message),
    path('<int:message_id>/delete_message', views.delete_message),
    path('clear', views.clear_notifications)
]