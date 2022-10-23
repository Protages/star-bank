from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


USER_MODEL = get_user_model()


@receiver(post_save, sender=USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
