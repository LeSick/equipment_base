from django.urls import path
from . import views

app_name = 'repairs'

urlpatterns = [
    path('', views.repairs_list, name='repairs_list'),
    path('add/', views.repairs_add, name='repairs_add'),
    path('ajax/get-shops/', views.get_shops, name='get_shops'),
    path('ajax/get-equipment-positions/', views.get_equipment_positions, name='get_equipment_positions'),
]