from django.urls import path
from . import views


urlpatterns = [
    path('entries/', views.stock_entry_list, name='stock_entry_list'),
    path('entries/add/', views.add_stock_entry, name='add_stock_entry'),
    path('entries/edit/<int:pk>/', views.edit_stock_entry, name='edit_stock_entry'),
    path('entries/delete/<int:pk>/', views.delete_stock_entry, name='delete_stock_entry'),
    path('outs/', views.stock_out_list, name='stock_out_list'),
    path('outs/add/', views.add_stock_out, name='add_stock_out'),
    path('outs/edit/<int:pk>/', views.edit_stock_out, name='edit_stock_out'),
    path('outs/delete/<int:pk>/', views.delete_stock_out, name='delete_stock_out'),
        path('export/', views.export_stock_data, name='export_stock_data'),  # Corrigé ici]

]