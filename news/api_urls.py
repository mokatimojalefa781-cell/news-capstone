from django.urls import path
from .api_views import ReaderSubscribedArticlesAPIView

app_name = "news_api"
urlpatterns = [
    path("subscribed-articles/", ReaderSubscribedArticlesAPIView.as_view(), name="reader_articles"),
]
