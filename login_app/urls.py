from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login),
    path('user_login', views.user_login),
    path('register', views.register),
    path('signup', views.signup),
    path('logout', views.logout),

    path('reset_password', views.password_reset_request, name = "reset_password"),
    
    # path('reset_password', auth_views.PasswordResetView.as_view(template_name = "pw_reset.html"), name = "reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name = "pw_reset_sent.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "pw_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name = "pw_reset_complete.html"), name = "password_reset_complete"),
]