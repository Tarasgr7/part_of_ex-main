from django.urls import path
from stats import views

urlpatterns = [
    path('statistics/', views.user_statistics, name='stats'),
]