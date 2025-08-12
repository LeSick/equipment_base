from django.contrib import admin
from .models import EquipmentPos, EquipmentName, EquipClass, EquipSubClass, Shop, Department, LegalEntity

@admin.register(EquipmentPos)
class EquipmentPosAdmin(admin.ModelAdmin):
    list_display = ('pos', 'shop', 'get_equip_class', 'equipment_name', 'legal_entity')
    def get_equip_class(self, obj):
        return obj.equipment_name.equip_class
    get_equip_class.short_description = 'Equipment Class'

@admin.register(EquipmentName)
class EquipmentNameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register other models as needed
admin.site.register(EquipClass)
admin.site.register(EquipSubClass)
admin.site.register(Shop)
admin.site.register(Department)
admin.site.register(LegalEntity)
