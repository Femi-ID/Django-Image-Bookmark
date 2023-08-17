from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like
    instance.save()
# You have to connect your receiver function to a signal so that it gets called every time the signal is sent.
# The recommended method for registering your signals is by importing them in the ready() method of your application configuration class

# pre_save(), post_save(), pre_delete, post_delete: These are just a subset of the signals provided by Django.
# You can find a list of all built-in signals at https://docs.djangoproject.com/en/3.0/ref/signals/.

