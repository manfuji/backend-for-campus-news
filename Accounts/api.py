from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from knox.models import AuthToken


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer


    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer


    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        _,token = AuthToken.objects.create(user)
        return Response({
            "user": LoginSerializer(user, context = self.get_serializer_context()).data,
            "token": token
        })


class GetUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        ]
    queryset = User.objects.all()