from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken




class InterCardlessAPIView(APIView):
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
            data = list(InterCardless.objects.values())
                        
            return Response({'requested': user_id, 'data': data})
        except Exception as ex:
            print(ex)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)



class IntraCardlessAPIView(APIView):
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
            data = list(IntraCardless.objects.values())
                        
            return Response({'requested': user_id, 'data': data})
        except Exception as ex:
            print(ex)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

