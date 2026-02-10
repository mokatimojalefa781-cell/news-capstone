from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("articles/", views.article_list, name="article_list"),
    path("publishers/", views.publisher_list, name="publisher_list"),
    path("journalist/dashboard/", views.journalist_dashboard, name="journalist_dashboard"),
    path("journalist/articles/create/", views.create_article, name="create_article"),
    path("journalist/newsletters/create/", views.create_newsletter, name="create_newsletter"),
    path("editor/pending/", views.pending_articles, name="pending_articles"),
    path("editor/approve/article/<int:pk>/", views.approve_article, name="approve_article"),
    path("editor/approve/newsletter/<int:pk>/", views.approve_newsletter, name="approve_newsletter"),
    path("editor/reject/article/<int:pk>/", views.reject_article, name="reject_article"),
    path("editor/reject/newsletter/<int:pk>/", views.reject_newsletter, name="reject_newsletter"),
    path("reader/subscribe/publishers/", views.subscribe_publishers, name="subscribe_publishers"),
    path("reader/subscribe/journalists/", views.subscribe_journalists, name="subscribe_journalists"),
]
