from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

class HomeController(APIView):
    http_method_names = ["get"]

    def get(self, request: Request) -> Response:
        return Response(data={"message": "testing home"})