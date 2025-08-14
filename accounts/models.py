from django.db import models

class RegistrationRequest(models.Model):
    email = models.EmailField(unique=True)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
