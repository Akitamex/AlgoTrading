from rest_framework import serializers
from .models import *

class InterCardlessSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterCardless
        fields = '__all__'

class IntraCardlessSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntraCardless
        fields = '__all__'

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'

class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = '__all__'
