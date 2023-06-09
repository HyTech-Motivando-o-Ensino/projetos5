from rest_framework import serializers

class ArticlePerStratumSerializer(serializers.Serializer):
    estrato = serializers.CharField(required=True)
    count = serializers.IntegerField(required=True)