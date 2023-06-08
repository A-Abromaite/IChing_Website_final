from django.urls import path
from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.index, name='index'),
    path('toss-coins/', views.toss_coins, name='toss_coins'),
    path('my-iching/', views.my_iching, name='my_iching'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('save_hexagram/', views.save_hexagram, name='save_hexagram'),
]