from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.serializers import UserSerializer, ReferalSerializer, SubscriptionSerializer, UserModelSerializer, RoleSerializer
from academy.models import Progress
from .models import CustomUser, Subscription, Role, Referal
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken


class UsersAPIView(APIView):
    def get(self, request, user_uuid=None):
        
        lst = CustomUser.objects.all().values()
        return Response({'users': list(lst)})
    
    def post(self, request, format=None):
        email = request.data.get('email')
        
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                if user:
                    return Response({'error': 'User with specified email already exists'}, status=status.HTTP_409_CONFLICT)
            except Exception:
                pass
                
            
                
        password = make_password(request.data.get('password'))
        request.data['password'] = password
        
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
        else:
            serializer.is_valid(raise_exception=True)
        
        subscription_serializer = Subscription.objects.create(user=user, role=Role.objects.get(name="Free"))
        subscription_serializer.save()
        
        progress = Progress.objects.create(user=user)
        progress.save()
        
        return Response(serializer.data)


class UserAPIUpdate(APIView):
    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            serializer = UserModelSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id, format=None):
        try:
            access_token = request.data['access_token']
        except KeyError:
            return Response({'error': 'access_token is not specified'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                user_id = decoded_token['user_id']
            except InvalidToken:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Access token not specified'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            new_password = request.data.get('password')
            new_password = make_password(new_password)
            request.data['password'] = new_password
        except KeyError:
            pass
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserAPIView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        
        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                user_id = decoded_token['user_id']
            except InvalidToken:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Access token not specified'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_subscription = Subscription.objects.get(user_id=user_id)
        subscription_serializer = SubscriptionSerializer(user_subscription)
        user = CustomUser.objects.get(id=user_id)
        serializer = UserModelSerializer(user)
        
        referalcode_id = serializer.data['referal']
        referal_serializer = None
        
        if referalcode_id:
            referal = Referal.objects.get(id=referalcode_id)
            referal_serializer = ReferalSerializer(referal)
        else:
            return Response({'user': serializer.data, 'subscription': subscription_serializer.data, 'referal': None})
            
        
        return Response({'user': serializer.data, 'subscription': subscription_serializer.data, 'referal': referal_serializer.data})


class ReferalAPIView(APIView):
    def get(self, request):
        referals = Referal.objects.all()
        serializer = ReferalSerializer(referals, many=True)
        return Response({'referals': serializer.data})
    
class RoleAPIView(APIView):
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response({'roles': serializer.data})
    
