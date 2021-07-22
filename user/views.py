from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        email=request.data["email"]
        password=request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        refresh=RefreshToken.for_user(user)
        return Response({'message':'You are successfully logged in!!','refresh': str(refresh),
        'access': str(refresh.access_token)})



class ProfileView(APIView):
    
    def get(self,request):
        authentication_classes=[JWTAuthentication]
        permission_classes=[IsAuthenticated]
        Serializer=UserSerializer(request.user)
        return Response(Serializer.data)