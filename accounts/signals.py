from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    user_model = get_user_model()
    permission_codenames = {
        "Reader": ["view_article", "view_newsletter"],
        "Editor": ["view_article", "change_article", "delete_article", "view_newsletter", "change_newsletter", "delete_newsletter"],
        "Journalist": ["add_article", "view_article", "change_article", "delete_article", "add_newsletter", "view_newsletter", "change_newsletter", "delete_newsletter"],
    }
    for group_name, codenames in permission_codenames.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        perms = Permission.objects.filter(codename__in=codenames)
        group.permissions.set(perms)

    for user in user_model.objects.all():
        role_group_name = user.role.title()
        group, _ = Group.objects.get_or_create(name=role_group_name)
        user.groups.set([group])
