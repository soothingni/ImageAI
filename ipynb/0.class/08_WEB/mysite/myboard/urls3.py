from django.urls import path
from . import views

urlpatterns = [
    path('<category>/<int:page>/', views.listsql, name='listsql'),
]
