from django.urls import path
from . import views

urlpatterns = [
    path('', views.search),
    path('<str:query>/people', views.search_people),
    path('<str:query>/pokemon', views.search_pokemon),
    path('<str:query>/all', views.search_all),
]