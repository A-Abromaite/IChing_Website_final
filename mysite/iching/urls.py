from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('toss-coins/', views.toss_coins, name='toss_coins'),
]