from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created: bool, **kwargs) -> None:
    """Ensure every user has an associated profile."""
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs) -> None:
    """Persist related profile when the user object is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
