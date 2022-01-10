from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('query_results', views.query_results, name='query_results'),
    path('run_query', views.run_query, name='run_query'),
    path('add_pokemon', views.add_pokemon, name='add_pokemon'),
    path('add', views.add, name='add')
]
