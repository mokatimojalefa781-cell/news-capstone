from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mass_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm, JournalistSubscriptionForm, NewsletterForm, PublisherSubscriptionForm
from .models import Article, Newsletter, Publisher

def user_is_editor(user):
    return user.is_authenticated and (user.role == "editor" or user.groups.filter(name="Editor").exists())

def user_is_journalist(user):
    return user.is_authenticated and user.role == "journalist"

def user_is_reader(user):
    return user.is_authenticated and user.role == "reader"

def home(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter(is_approved=True).select_related("publisher", "journalist")
    newsletters = Newsletter.objects.filter(is_approved=True).select_related("publisher", "journalist")
    return render(request, "news/home.html", {"articles": articles, "newsletters": newsletters})

@login_required
def article_list(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter(is_approved=True).select_related("publisher", "journalist")
    return render(request, "news/article_list.html", {"articles": articles})

@login_required
@user_passes_test(user_is_journalist)
def create_article(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.journalist = request.user
            article.is_approved = False
            article.save()
            messages.success(request, "Article created and sent for approval.")
            return redirect("journalist_dashboard")
    else:
        form = ArticleForm()
    return render(request, "news/create_article.html", {"form": form, "type": "Article"})

@login_required
@user_passes_test(user_is_journalist)
def create_newsletter(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.journalist = request.user
            newsletter.is_approved = False
            newsletter.save()
            messages.success(request, "Newsletter created and sent for approval.")
            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm()
    return render(request, "news/create_article.html", {"form": form, "type": "Newsletter"})

@login_required
@user_passes_test(user_is_journalist)
def journalist_dashboard(request: HttpRequest) -> HttpResponse:
    articles = request.user.articles.all().select_related("publisher")
    newsletters = request.user.newsletters.all().select_related("publisher")
    return render(request, "news/journalist_dashboard.html", {"articles": articles, "newsletters": newsletters})

@login_required
@user_passes_test(user_is_editor)
def pending_articles(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter(is_approved=False).select_related("publisher", "journalist")
    newsletters = Newsletter.objects.filter(is_approved=False).select_related("publisher", "journalist")
    return render(request, "news/pending.html", {"articles": articles, "newsletters": newsletters})

def _send_to_subscribers(title: str, content: str, publisher, journalist) -> None:
    subscriber_emails = set()
    if publisher:
        subscriber_emails.update(publisher.subscribers.exclude(email="").values_list("email", flat=True))
    subscriber_emails.update(journalist.reader_subscribers.exclude(email="").values_list("email", flat=True))
    if subscriber_emails:
        email_payload = ("New publication approved", f"{title}\n\n{content}", None, list(subscriber_emails))
        send_mass_mail((email_payload,), fail_silently=True)

@login_required
@user_passes_test(user_is_editor)
def approve_article(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk, is_approved=False)
    article.is_approved = True
    article.approved_by = request.user
    article.save(update_fields=["is_approved", "approved_by"])
    _send_to_subscribers(article.title, article.content, article.publisher, article.journalist)
    messages.success(request, "Article approved and distributed to subscribers.")
    return redirect("pending_articles")

@login_required
@user_passes_test(user_is_editor)
def approve_newsletter(request: HttpRequest, pk: int) -> HttpResponse:
    newsletter = get_object_or_404(Newsletter, pk=pk, is_approved=False)
    newsletter.is_approved = True
    newsletter.save(update_fields=["is_approved"])
    _send_to_subscribers(newsletter.title, newsletter.content, newsletter.publisher, newsletter.journalist)
    messages.success(request, "Newsletter approved and distributed to subscribers.")
    return redirect("pending_articles")

@login_required
@user_passes_test(user_is_editor)
def reject_article(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk, is_approved=False)
    article.delete()
    messages.info(request, "Article rejected and removed.")
    return redirect("pending_articles")

@login_required
@user_passes_test(user_is_editor)
def reject_newsletter(request: HttpRequest, pk: int) -> HttpResponse:
    newsletter = get_object_or_404(Newsletter, pk=pk, is_approved=False)
    newsletter.delete()
    messages.info(request, "Newsletter rejected and removed.")
    return redirect("pending_articles")

@login_required
@user_passes_test(user_is_reader)
def subscribe_publishers(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PublisherSubscriptionForm(request.POST)
        if form.is_valid():
            request.user.subscribed_publishers.set(form.cleaned_data["publishers"])
            messages.success(request, "Publisher subscriptions updated.")
            return redirect("home")
    else:
        form = PublisherSubscriptionForm(initial={"publishers": request.user.subscribed_publishers.all()})
    return render(request, "news/subscribe_publishers.html", {"form": form})

@login_required
@user_passes_test(user_is_reader)
def subscribe_journalists(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = JournalistSubscriptionForm(request.POST)
        if form.is_valid():
            request.user.subscribed_journalists.set(form.cleaned_data["journalists"])
            messages.success(request, "Journalist subscriptions updated.")
            return redirect("home")
    else:
        form = JournalistSubscriptionForm(initial={"journalists": request.user.subscribed_journalists.all()})
    return render(request, "news/subscribe_journalists.html", {"form": form})

@login_required
def publisher_list(request: HttpRequest) -> HttpResponse:
    publishers = Publisher.objects.all().prefetch_related("editors", "journalists")
    return render(request, "news/publisher_list.html", {"publishers": publishers})
