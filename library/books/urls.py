from django.urls import path 
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('listbook/', views.ListBook.as_view(), name='list-book'),
    path('create/', views.CreateBook.as_view(), name='create')
]