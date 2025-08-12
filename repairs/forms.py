from django import forms
from .models import Repairs
from equipment.models import EquipmentPos, Shop

class RepairsForm(forms.ModelForm):
    shop = forms.ModelChoiceField(queryset=Shop.objects.none(), required=True)

    class Meta:
        model = Repairs
        fields = [
            'legal_entity', 'shop', 'equipment_pos', # Added 'shop'
            'start', 'end', 'reason', 'job', 'duration', 'note'
        ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, filter shops by legal_entity if instance or initial is set
        if 'legal_entity' in self.data:
            legal_entity_id = self.data.get('legal_entity')
            self.fields['shop'].queryset = Shop.objects.filter(legal_entity_id=legal_entity_id)
        elif self.instance.pk:
            self.fields['shop'].queryset = Shop.objects.filter(legal_entity=self.instance.legal_entity)
        else:
            self.fields['shop'].queryset = Shop.objects.none()

        # Filter equipment_pos based on legal_entity and shop
        if 'legal_entity' in self.data and 'shop' in self.data:
            legal_entity_id = self.data.get('legal_entity')
            shop_id = self.data.get('shop')
            self.fields['equipment_pos'].queryset = EquipmentPos.objects.filter(
                legal_entity_id=legal_entity_id, shop_id=shop_id
            )
        elif self.instance.pk:
            self.fields['equipment_pos'].queryset = EquipmentPos.objects.filter(
                legal_entity=self.instance.legal_entity, shop=self.instance.shop
            )
        else:
            self.fields['equipment_pos'].queryset = EquipmentPos.objects.none()