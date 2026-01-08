from django.urls import path
from . import views

app_name = 'music_recommender'

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend/', views.recommend, name='recommend'),
]