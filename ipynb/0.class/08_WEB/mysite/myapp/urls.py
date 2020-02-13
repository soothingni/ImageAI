from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('test/', views.test),
    path('login/', views.login),
    path('service/', views.service),
    path('uploadimage/', views.uploadimage),
]