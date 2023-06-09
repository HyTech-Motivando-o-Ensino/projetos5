from rest_framework import serializers

class AuthorWithSupervisionSerializer(serializers.Serializer):
    nome_completo = serializers.CharField(required=True)
    trabalho_conclusao_graduacao = serializers.IntegerField()
    dissertacao_mestrado = serializers.IntegerField()
    tese_doutorado = serializers.IntegerField()
    trabalho_iniciacao_cientifica = serializers.IntegerField()