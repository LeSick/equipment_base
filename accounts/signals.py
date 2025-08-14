from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import RegistrationRequest

@receiver(post_save, sender=RegistrationRequest)
def create_user_on_approval(sender, instance, **kwargs):
    if instance.approved and not User.objects.filter(username=instance.email).exists():
        User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password=User.objects.make_random_password()
        )