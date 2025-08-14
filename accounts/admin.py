from django.contrib import admin
from .models import RegistrationRequest

class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'approved', 'requested_at')
    list_filter = ('approved',)

admin.site.register(RegistrationRequest, RegistrationRequestAdmin)
