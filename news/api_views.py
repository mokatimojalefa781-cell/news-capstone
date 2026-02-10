from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer

class ReaderSubscribedArticlesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "reader":
            return Response({"detail": "Only readers can use this endpoint."}, status=403)

        articles = (
            Article.objects.filter(is_approved=True)
            .filter(Q(publisher__in=user.subscribed_publishers.all()) | Q(journalist__in=user.subscribed_journalists.all()))
            .select_related("publisher", "journalist")
            .distinct()
            .order_by("-created_at")
        )
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
