from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_verification_email


@receiver(post_save, sender=User)
def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_active:
        send_verification_email.delay(instance.pk)
