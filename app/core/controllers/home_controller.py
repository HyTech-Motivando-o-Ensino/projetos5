from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Autor
from core.serializers import AuthorSerializer

class HomeController(APIView):
    http_method_names = ["get"]

    def get(self, request: Request) -> Response:
        instance = Autor.objects.all()

        return Response(data=AuthorSerializer(instance, many=True).data)