"""
Models for the accounts app.

This module defines custom user-related models used in the News Application.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    This model allows future extension of user-related fields
    without changing Django's default authentication behavior.
    """

    def __str__(self):
        """
        Return the string representation of the user.
        """
        return self.username

