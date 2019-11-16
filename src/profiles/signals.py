from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    if instance.status == 'accepted':
        sender.friends.add(receiver)
        receiver.friends.add(receiver)
        sender.save()
        receiver.save()


@receiver(post_save, sender=Relationship)
def post_save_remove_from_friends(sender, created, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    if instance.status == 'deleted':
        sender.friends.remove(receiver)
        receiver.friends.remove(receiver)
        sender.save()
        receiver.save()
