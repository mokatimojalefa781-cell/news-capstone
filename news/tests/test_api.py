from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from news.models import Article, Publisher

class ReaderSubscriptionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_model = get_user_model()
        self.reader = user_model.objects.create_user(username="reader1", password="pass12345", role="reader")
        self.journalist = user_model.objects.create_user(username="journalist1", password="pass12345", role="journalist")
        self.journalist_two = user_model.objects.create_user(username="journalist2", password="pass12345", role="journalist")

        self.publisher = Publisher.objects.create(name="Daily News")
        self.publisher.journalists.add(self.journalist)

        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

        self.matching_article = Article.objects.create(
            title="Matched Article", content="Visible to this reader", is_approved=True,
            journalist=self.journalist, publisher=self.publisher,
        )
        Article.objects.create(title="Unmatched Article", content="Should not be included", is_approved=True, journalist=self.journalist_two)
        Article.objects.create(title="Pending Article", content="Pending status should hide this", is_approved=False, journalist=self.journalist, publisher=self.publisher)

    def test_reader_gets_only_subscribed_approved_articles(self):
        self.client.login(username="reader1", password="pass12345")
        url = reverse("news_api:reader_articles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.matching_article.id)

    def test_non_reader_is_forbidden(self):
        self.client.login(username="journalist1", password="pass12345")
        url = reverse("news_api:reader_articles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
