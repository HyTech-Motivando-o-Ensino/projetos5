from rest_framework import serializers

from .article_per_year_serializer import ArticlePerYearSerializer
from .article_per_stratum_serializer import ArticlePerStratumSerializer
from .article_per_field_serializer import ArticlePerFieldSerializer
from .author_with_supervision_serializer import AuthorWithSupervisionSerializer

class DashboardSerializer(serializers.Serializer):
    total_articles = serializers.IntegerField(required=True)
    articles_in_last_triennium = serializers.IntegerField(required=True)
    supervisions_in_last_triennium = serializers.IntegerField(required=True)
    articles_per_year = serializers.ListField(child=ArticlePerYearSerializer())
    articles_per_stratum = serializers.ListField(child=ArticlePerStratumSerializer())
    articles_per_field = serializers.ListField(child=ArticlePerFieldSerializer())
    authors_with_supervision_count = serializers.ListField(child=AuthorWithSupervisionSerializer())
