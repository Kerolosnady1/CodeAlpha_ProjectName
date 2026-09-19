from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_home, name='restaurant_home'),
    path('order/', views.place_order, name='place_order'),
    ]
