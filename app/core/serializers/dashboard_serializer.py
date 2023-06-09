from rest_framework import serializers

from .article_per_year_serializer import ArticlePerYearSerializer
from .article_per_stratum_serializer import ArticlePerStratumSerializer
from .article_per_field_serializer import ArticlePerFieldSerializer

class DashboardSerializer(serializers.Serializer):
    articles_per_year = serializers.ListField(child=ArticlePerYearSerializer())
    articles_per_stratum = serializers.ListField(child=ArticlePerStratumSerializer())
    articles_per_field = serializers.ListField(child=ArticlePerFieldSerializer())
