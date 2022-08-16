from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_organizer = models.BooleanField(default=False)
    is_agent = models.BooleanField(
        default=False,
    )

    def clean(self):
        super().clean()
        if self.is_organizer and self.is_agent:
            raise ValidationError("User can't be Agent and Organizer at the same time")
