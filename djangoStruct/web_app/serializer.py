from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ReactSerializer(serializers.ModelSerializer):
	class Meta:
		model = React
		fields = ['name', 'detail']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=24, write_only=True)

    def validate(self, data):  
        # Getting the username and password and passing it into the authenticate function (from django's auth module)
        user = authenticate(username = data.get('username'), password = data.get('password'))
        if user and user.is_active:
            return user
        if not user.is_active:
            raise serializers.ValidationError("Inactive User")
        # Reached here after the user is None (user is returned None when authentication fails)
        raise serializers.ValidationError("Invalid Authentication Credentials")
    
    
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True, max_length=8)
    password = serializers.CharField(write_only=True, required=True, max_length=24)
    #TODO: Have extra fields for {ucalgary_email, First Name, Last Name}
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwarg = {'password':{'write_only':True}, 'password':{'required': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        return user