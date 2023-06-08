from rest_framework import serializers
from core.models import Autor

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = [
            'created_at',
            'updated_at',
            'nome_completo',
            'resumo_cv',
            'colaborador_cesar',
        ]

