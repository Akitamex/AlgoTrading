from django.urls import path
from .views import *

urlpatterns = [
    path("inter/", InterCardlessAPIView.as_view(), name="intercardlessview"),
    path("intra/", IntraCardlessAPIView.as_view(), name="intracardlessview"),
]
