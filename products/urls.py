from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicament_list, name='medicament_list'),
    path('add/', views.medicament_add, name='medicament_add'),
    path('<int:pk>/edit/', views.medicament_edit, name='medicament_edit'),
    path('<int:pk>/delete/', views.medicament_delete, name='medicament_delete'),
    path('history/', views.medicament_history, name='medicament_history'),
]
