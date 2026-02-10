from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source="publisher.name", read_only=True)
    journalist_username = serializers.CharField(source="journalist.username", read_only=True)

    class Meta:
        model = Article
        fields = ["id","title","content","publisher","publisher_name","journalist","journalist_username","is_approved","created_at"]
