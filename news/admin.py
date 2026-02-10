from django.contrib import admin
from .models import Article, Newsletter, Publisher


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "journalist", "publisher", "is_approved", "created_at")
    list_filter = ("is_approved", "publisher")
    search_fields = ("title", "content")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("title", "journalist", "publisher", "is_approved", "created_at")
    list_filter = ("is_approved", "publisher")
    search_fields = ("title", "content")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)


