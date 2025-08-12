from django.db import models

# Create your models here.

class LegalEntity(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=45)
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.CASCADE)  # Updated to reference LegalEntity directly

    def __str__(self):
        return self.name

class Shop(models.Model):
    name = models.CharField(max_length=45)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class EquipClass(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class EquipSubClass(models.Model):
    name = models.CharField(max_length=45)
    equip_class = models.ForeignKey(EquipClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class EquipmentName(models.Model):
    name = models.CharField(max_length=100)
    equip_class = models.ForeignKey('EquipClass', on_delete=models.SET_NULL, null=True, blank=True)
    equip_subclass = models.ForeignKey('EquipSubClass', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class EquipmentPos(models.Model):
    pos = models.CharField(max_length=10)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.CASCADE, null=True, blank=True)
    equipment_name = models.ForeignKey(EquipmentName, on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return self.pos