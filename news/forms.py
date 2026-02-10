from django import forms
from accounts.models import CustomUser
from .models import Article, Newsletter, Publisher

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "publisher"]

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["title", "content", "publisher"]

class PublisherSubscriptionForm(forms.Form):
    publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )

class JournalistSubscriptionForm(forms.Form):
    journalists = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role=CustomUser.Roles.JOURNALIST),
        required=False, widget=forms.CheckboxSelectMultiple
    )
