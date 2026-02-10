from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        READER = "reader", "Reader"
        EDITOR = "editor", "Editor"
        JOURNALIST = "journalist", "Journalist"

    role = models.CharField(max_length=20, choices=Roles.choices)

    #  ADDED FIELD
    subscribed_publishers = models.ManyToManyField(
        "news.Publisher",
        blank=True,
        related_name="subscribers"
    )

    def save(self, *args, **kwargs):
        if self.role == self.Roles.EDITOR:
            self.is_staff = True
        elif self.role == self.Roles.READER:
            self.is_staff = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
