from django.shortcuts import get_object_or_404, render
from post.uploads import S3ImgUploader
from django.contrib.auth import authenticate, logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import User, Profile
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, ProfileSerializer
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

            profile = Profile.objects.get(user=user)

            nickname = request.data.get('nickname')
            age = request.data.get('age')
            gender = request.data.get('gender')
            height = request.data.get('height')
            start_weight = request.data.get('start_weight')
            goal_weight = request.data.get('goal_weight')
            about = request.data.get('about')
            
            try:
                image = request.FILES['image']
            except:
                is_image = False
            else:
                is_image = True


            profile_data = {
                "user": user.id,
                "nickname": nickname,
                "age": age,
                "gender": gender,
                "height": height,
                "start_weight": start_weight,
                "goal_weight": goal_weight,
                "about": about
            }

            if not (nickname and age and gender and height and start_weight and goal_weight and about):
                user.delete()
                return Response({"error":"프로필 정보를 입력해주세요."},status=status.HTTP_400_BAD_REQUEST)
            
            if is_image:
                img_uploader = S3ImgUploader(image)
                folder = 'post_image'
                uploaded_url = img_uploader.upload(folder)
                profile_data['image'] = uploaded_url
                
            pf_serializer = ProfileSerializer(profile, profile_data)

            if pf_serializer.is_valid():
                pf_serializer.save()
            else:
                return Response(pf_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            message = {
                "message": "회원가입 성공",
                "user": pf_serializer.data,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                }
            }

            return Response(message, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
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
        else: 
            return Response({"error" : "이메일 또는 비밀번호가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        

# 로그아웃 
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        refresh_token = RefreshToken.for_user(user)
        refresh_token.blacklist()
        logout(request)
        return Response({"message":"로그아웃 성공"},status=status.HTTP_200_OK)


# 프로필 조회
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id=None):
        if user_id is None:
            user = request.user
        else:
            user = get_object_or_404(User, pk=user_id)
        profile = get_object_or_404(Profile, user=user)
        pf_serializer = ProfileSerializer(profile, context={'request':request})

        profile_data = pf_serializer.data
        profile_data['image'] = profile.image
        
        data = {
            'profile': profile_data
        }

        return Response(data, status=status.HTTP_200_OK)