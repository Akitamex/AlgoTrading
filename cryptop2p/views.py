from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

class CryptoAPIView(APIView):
    def get(self, request):
        return Response({'error': 'GET doesn\'t exists'}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def post(self, request):
        access_token = request.data['access_token']
        
        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                user_id = decoded_token['user_id']
            except InvalidToken:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Access token not specified'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:            
            data = list(CryptoP2p.objects.values())
            
            if request.data.get('fiat'):
                if len(request.data.get('fiat')) > 1:
                    for i in range(len(data)-1, -1, -1):
                        if request.data.get('fiat') != data[i]['data']['Fiat']:
                            data.pop(i)
            
            if request.data.get('buy_bank'):
                if len(request.data.get('buy_bank')) > 1:
                    for i in range(len(data)-1, -1, -1):
                        if request.data.get('buy_bank') not in data[i]['data']['Buy banks']:
                            data.pop(i)

            if request.data.get('sell_bank'):
                if len(request.data.get('sell_bank')) > 1:
                    for i in range(len(data)-1, -1, -1):
                        if request.data.get('sell_bank') not in data[i]['data']['Sell banks']:
                            data.pop(i)
                            
            if request.data.get('asset'):
                if len(request.data.get('asset')) > 1:
                    for i in range(len(data)-1, -1, -1):
                        if request.data.get('asset') != data[i]['data']['Asset']:
                            data.pop(i)
                            
            if request.data.get('exchange'):
                if len(request.data.get('exchange')) > 1:
                    for i in range(len(data)-1, -1, -1):
                        if request.data.get('exchange') != data[i]['data']['Type']:
                            data.pop(i)
            
            return Response({'requested': user_id, 'data': data})
        except Exception as ex:
            print(ex)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        
class AvailableCryptoFiatsAPIView(APIView):
    def get(self, request):
        modelObjects = Fiat.objects.all()
        dataSerializer = FiatSerializer(modelObjects, many=True).data
        
        data = []
        
        for item in dataSerializer:
            data.append(item)
        
        return Response({'fiats': list(data)})
        
        
            
class AvailableCryptoExchangesAPIView(APIView):
    def get(self, request):
        modelObjects = Exchange.objects.all()
        dataSerializer = ExchangeSerializer(modelObjects, many=True).data
        
        data = []
        
        for item in dataSerializer:
            data.append(item)
        
        return Response({'exchanges': list(data)})
        
class AvailableCryptoBanksAPIView(APIView):
    def get(self, request):
        modelObjects = Bank.objects.all()
        dataSerializer = BankSerializer(modelObjects, many=True).data
        
        data = []
        
        for item in dataSerializer:
            data.append(item)
        
        return Response({'banks': list(data)})

class AvailableCryptoAssetsAPIView(APIView):
    def get(self, request):
        modelObjects = Asset.objects.all()
        dataSerializer = AssetSerializer(modelObjects, many=True).data
        
        data = []
        
        for item in dataSerializer:
            data.append(item)
        
        return Response({'assets': list(data)})        
