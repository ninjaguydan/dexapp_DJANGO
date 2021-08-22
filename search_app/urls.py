from django.urls import path
from . import views

urlpatterns = [
    path('', views.search),
    path('dex', views.dex),
    # path('dex-filtered', )
]