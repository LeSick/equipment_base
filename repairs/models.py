from django.db import models

class RepairType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'repair_type'

class Repairs(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    reason = models.ForeignKey('Reason', on_delete=models.SET_NULL, null=True, blank=True)
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.FloatField()
    note = models.TextField(blank=True, null=True)
    repair_type = models.ForeignKey('RepairType', on_delete=models.SET_NULL, null=True, blank=True)
    legalentity = models.ForeignKey('equipment.LegalEntity', on_delete=models.SET_NULL, null=True, blank=True)
    pos = models.ForeignKey('equipment.EquipmentPos', on_delete=models.SET_NULL, null=True, blank=True)
    shop = models.ForeignKey('equipment.Shop', on_delete=models.SET_NULL, null=True, blank=True)
    equipment_name = models.ForeignKey('equipment.EquipmentName', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'repairs_journal_new'

class Reason(models.Model):
    reason = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'repairs_reasons'

class Job(models.Model):
    job = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'repairs_jobs'
