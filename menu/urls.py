from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu_page, name='menu'),

    path('add/', views.add_dish, name='add_dish'),
    path('<int:pk>/edit/', views.edit_dish, name='edit_dish'),
    path('<int:pk>/delete/', views.delete_dish, name='delete_dish'),
   
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]