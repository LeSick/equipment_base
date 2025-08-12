from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('add/', views.equipment_create, name='equipment_create'),
    path('equipment_list/', views.equipment_list, name='equipment_list'),
    path('equipment_list/<int:entity_id>/', views.equipment_list, name='equipment_list'),
    path('equipment_list/<int:entity_id>/<int:class_id>/', views.equipment_list, name='equipment_list'),
    path('equipment_list/<int:entity_id>/<int:class_id>/<int:subclass_id>/', views.equipment_list, name='equipment_list'),
    path('equipment_list/<int:entity_id>/<int:class_id>/<int:subclass_id>/<int:department_id>/', views.equipment_list, name='equipment_list'),
    path('equipment_list/<int:entity_id>/<int:class_id>/<int:subclass_id>/<int:department_id>/<int:shop_id>/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:name_id>/edit/', views.equipment_edit, name='equipment_edit'),
    path('ajax/get_classes/<int:entity_id>/', views.get_classes_by_entity, name='get_classes_by_entity'),
    path('ajax/get_subclasses/<int:class_id>/', views.get_subclasses_by_class, name='get_subclasses_by_class'),
]