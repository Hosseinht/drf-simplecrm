from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Agent, OrganizerUser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_organizer_user(sender, instance, created, **kwargs):
    if created and instance.is_organizer:
        OrganizerUser.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_organizer_user(sender, instance, **kwargs):
    agent = Agent.objects.filter(user__username=instance.username)
    """
        User can't be organizer and agent at the same time. if user is an agent first delete the agent instance
        and then make it an organizer
    """
    try:
        if instance.is_organizer:
            agent.delete()
            instance.organizeruser.save()

    except OrganizerUser.DoesNotExist:
        OrganizerUser.objects.create(user=instance)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_organizer_user(sender, instance, **kwargs):
    try:
        instance.organizeruser.delete()
    except OrganizerUser.DoesNotExist:
        pass


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_agent_user(sender, instance, created, **kwargs):
    if created and instance.is_agent:
        Agent.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_agent_user(sender, instance, **kwargs):
    organizer = OrganizerUser.objects.filter(user__username=instance.username)
    """
        User can't be organizer and agent at the same time. if user is an organizer first delete the organizer instance
        and then make it an agent
    """
    try:
        if instance.is_agent:
            organizer.delete()
            instance.agent.save()

    except Agent.DoesNotExist:
        Agent.objects.create(user=instance)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_agent_user(sender, instance, **kwargs):
    try:
        instance.agent.delete()
    except Agent.DoesNotExist:
        pass
