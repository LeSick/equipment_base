from django import forms
from .models import EquipmentPos, EquipmentName, EquipClass, EquipSubClass, Shop, Department, LegalEntity
from django.forms import inlineformset_factory

class EquipmentPosForm(forms.ModelForm):
    legal_entity = forms.ModelChoiceField(
        queryset=LegalEntity.objects.all(),
        required=False,
        label="Legal Entity"
    )
    shop = forms.ModelChoiceField(
        queryset=Shop.objects.all(),
        label="Shop"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label="Department"
    )
    
    equipment_name = forms.ModelChoiceField(
        queryset=EquipmentName.objects.all(),
        label="Equipment Name"
    )

    class Meta:
        model = EquipmentPos
        fields = ['pos', 'shop', 'department', 'legal_entity', 'equipment_name']

class EquipmentNameForm(forms.ModelForm):
    equip_class = forms.ModelChoiceField(
        queryset=EquipClass.objects.all(),
        required=False,
        label="Equipment Class"
    )
    equip_subclass = forms.ModelChoiceField(
        queryset=EquipSubClass.objects.all(),
        required=False,
        label="Equipment Subclass"
    )

    class Meta:
        model = EquipmentName
        fields = '__all__'

EquipmentPosFormSet = inlineformset_factory(
    EquipmentName, EquipmentPos, form=EquipmentPosForm, extra=0, can_delete=True
)