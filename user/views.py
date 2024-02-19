from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests

# Create your views here.



class Join(APIView):
    def post(self, request):
        
        user_data = {
            "email" : request.data.get('email'),
            "password" : request.data.get('password')
        }

        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()

            users_data = {
                "user": user.id,
            }

            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            message = {
                "message": "회원가입 성공",
                "user": users_data,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                }
            }

            return Response(message, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            email = email,
            password = password
        )

        if user is not None and user.is_active:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : user.id,
                    "message" : "Login success",
                    "token" : {
                        "access" : access_token,
                        "refresh" : refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else : 
            return Response({"error" : "이메일 또는 비밀번로가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)