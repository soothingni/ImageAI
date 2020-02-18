from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    #path('<name>/', views.index2),    #파라미터로 name을 넘겨줄 테니까 index2에서 받아서 써라.
    #path('<int:pk>/detail', views.index3),  #파라미터로 int형의 pk를 넘겨줄 테니까 index3에서 받아서 써라.
    path('list/', views.list, name='list'),    #name을 지정하면 이걸로 경로를 호출할 수 있다
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('add/', views.PostView.as_view(), name='add'),  #.as_view(): class를 view로 호출하기
    path('<int:pk>/edit/', views.PostEditView.as_view(), name='edit'),
]