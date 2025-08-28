from django import forms
from .models import Repairs, Job, Reason, RepairType
from equipment.models import EquipmentPos, Shop, LegalEntity, EquipmentName

class RepairsForm(forms.ModelForm):
    job = forms.ModelChoiceField(queryset=Job.objects.all(), required=False)
    reason = forms.ModelChoiceField(queryset=Reason.objects.all(), required=False)
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), required=False)
    pos = forms.ModelChoiceField(queryset=EquipmentPos.objects.all(), required=False)
    legalentity = forms.ModelChoiceField(queryset=LegalEntity.objects.all(), required=False)
    equipment_name = forms.ModelChoiceField(queryset=EquipmentName.objects.all(), required=False)
    repair_type = forms.ModelChoiceField(queryset=RepairType.objects.all(), required=False)

    class Meta:
        model = Repairs
        fields = [
            'start', 'end', 'reason', 'job', 'duration', 'note',
            'repair_type', 'legalentity', 'pos', 'shop', 'equipment_name'
        ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }