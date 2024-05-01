from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken


@receiver(post_save, sender=User)
def create_jwt_token(sender, instance=None, created=False, **kwargs):
    if created:
        RefreshToken.for_user(instance)
