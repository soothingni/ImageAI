from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    # path('', views.list),
    path('ajaxdel/', views.ajaxdel),
    path('ajaxget/', views.ajaxget),
    path('<category>/<int:pk>/<mode>/', views.BoardView.as_view(), name='myboard'),
    path('', lambda request: redirect('myboard', 'common', 0, 'list')),
]
