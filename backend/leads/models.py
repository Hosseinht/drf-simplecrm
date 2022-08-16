from django.conf import settings
from django.db import models
from django.utils import timezone


class UsersManager(models.Manager):
    """
        preload users. so django won't make extra queries for each single user
    """

    def get_queryset(self):
        return super().get_queryset().select_related("user")


class OrganizerUser(models.Model):
    """
        This user organize and manage Agents and Leads.
        Organizer User can see,update and delete a lead.
        Organizer User can't see and manage other organizer's Lead
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = UsersManager()

    def __str__(self):
        return self.user.username


class Agent(models.Model):
    """
        Agen can see the leads that assigned by the organizer.
        Agent can not edit or delete a lead
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    organizer = models.ForeignKey(
        OrganizerUser, blank=True, null=True, on_delete=models.CASCADE
    )

    objects = UsersManager()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Lead(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    age = models.IntegerField(default=0)
    organizer = models.ForeignKey(OrganizerUser, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    converted_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
