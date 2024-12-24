from django.urls import path
from . import views

urlpatterns = [
    path('', views.site_list, name='site_list'),
    path('create/', views.site_create, name='site_create'),
    path('<str:user_site_name>/<path:path>', views.proxy_view, name='proxy_view'),
]
