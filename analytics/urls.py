from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user_stats/', views.user_stats, name='user_stats')
]