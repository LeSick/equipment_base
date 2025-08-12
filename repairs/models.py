from django.db import models
from equipment.models import EquipmentPos, LegalEntity

# Create your models here.
class Repairs(models.Model):
    equipment_pos = models.ForeignKey(EquipmentPos, on_delete=models.CASCADE, related_name='repair')
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    duration = models.FloatField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Repair for {self.equipment_pos.pos} ({self.start} to {self.end})"
