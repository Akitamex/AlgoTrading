from rest_framework import serializers
from .models import *

class CryptoP2pSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoP2p
        fields = '__all__'

class AllCryptoP2pSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllCryptoP2p
        fields = '__all__'

class FiatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fiat
        fields = '__all__'

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'
        

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


