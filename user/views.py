from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.views import APIView
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
