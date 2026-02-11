"""
Views for the News application.

This module contains view functions responsible for rendering pages
and handling article- and newsletter-related actions such as creation,
approval, subscription, and listing.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mass_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import (
    ArticleForm,
    JournalistSubscriptionForm,
    NewsletterForm,
    PublisherSubscriptionForm,
)
from .models import Article, Newsletter, Publisher


# --- User role checks ---
def user_is_editor(user):
    """Check if the user is an editor."""
    return user.is_authenticated and (
        user.role == "editor" or user.groups.filter(name="Editor").exists()
    )


def user_is_journalist(user):
    """Check if the user is a journalist."""
    return user.is_authenticated and user.role == "journalist"


def user_is_reader(user):
