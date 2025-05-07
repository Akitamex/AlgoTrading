from django.urls import path
from .views import *

urlpatterns = [
    path("", CryptoAPIView.as_view(), name="crytop2pview"),
    path("fiats/", AvailableCryptoFiatsAPIView.as_view(), name="availablefiats"),
    path("exchanges/", AvailableCryptoExchangesAPIView.as_view(), name="availableexchanges"),
    path("banks/", AvailableCryptoBanksAPIView.as_view(), name="availablebanks"),
    path("assets/", AvailableCryptoAssetsAPIView.as_view(), name="availableassets"),
]
