from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from AllModels.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","email","password")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","email","password")
        extra_kwargs = {"password":{"write_only":True},}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data["username"],validated_data["email"],
        validated_data["password"])
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("invalid credentials")    


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['prouser']

    def validate(self,attrs):
        attrs['prouser'] = self.context['request'].user
        return attrs

    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['prouser'] = UserSerializer(instance.prouser).data
        return response


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
