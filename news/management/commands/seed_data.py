from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import Publisher, Article

class Command(BaseCommand):
    help = 'Seed initial data for the news app'

    def handle(self, *args, **kwargs):
        user_model = get_user_model()

        editor = user_model.objects.create_user(
            username='editor1', password='password123', role='editor'
        )
        journalist = user_model.objects.create_user(
            username='journalist1', password='password123', role='journalist'
        )

        publisher = Publisher.objects.create(name='Daily News')
        publisher.editors.add(editor)
        publisher.journalists.add(journalist)

        Article.objects.create(
            title='Sample Article',
            content='This is a sample approved article.',
            journalist=journalist,
            publisher=publisher,
            is_approved=True,
            approved_by=editor,
        )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
