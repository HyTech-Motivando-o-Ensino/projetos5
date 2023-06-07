from django.urls import path
from core.controllers import (
    HomeController, DashboardController)


urlpatterns = [
    path('', HomeController.as_view(), name='home'),
    path('dashboard/', DashboardController.as_view(), name='dashboard'),
]