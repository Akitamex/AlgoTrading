from rest_framework import serializers
from .models import CustomUser, Role, Referal, Subscription


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    referal = serializers.CharField(required=False)
    
    def create(self, validated_data):
        referal_code = validated_data.get('referal')
        
        if referal_code:
            try:
                referal = Referal.objects.get(referal_code=referal_code)
            except Referal.DoesNotExist:
                raise serializers.ValidationError('Invalid referral code')
        else:
            referal = None
        
        validated_data['referal'] = referal
        return CustomUser.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
    
    
    
class ReferalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referal
        fields = '__all__'
        

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        

