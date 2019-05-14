
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


# Creates a user profile when the user signs up to the page
# and provides a default avatar


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwarks):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwarks):
    instance.profile.save()
