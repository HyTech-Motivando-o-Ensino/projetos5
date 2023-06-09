
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.repositories import DashboardRepository
from core.serializers import DashboardSerializer


class DashboardController(APIView):
    http_method_names = ["get"]
    def __init__(self):
        self.__dashboard_repository = DashboardRepository()

    def get(self, request: Request) -> Response:
        results = self.__dashboard_repository.get_dashboard_data()
        data = DashboardSerializer(results).data

        return Response(data=data)