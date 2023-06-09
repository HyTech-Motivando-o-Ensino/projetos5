from rest_framework import serializers

class ArticlePerFieldSerializer(serializers.Serializer):
    label = serializers.CharField(required=True)
    value = serializers.IntegerField(required=True)