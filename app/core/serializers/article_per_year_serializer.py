from rest_framework import serializers

class ArticlePerYearSerializer(serializers.Serializer):
    ano = serializers.CharField(required=True)
    count = serializers.IntegerField(required=True)