"""
Forms for user registration and authentication.

This module contains Django forms related to the CustomUser model.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form used to create new users.

    Extends Django's UserCreationForm to work with CustomUser.
    """

    class Meta:
        """
        Meta configuration for the form.
        """
        model = CustomUser
        fields = ("username", "email")

