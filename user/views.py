from django.shortcuts import render, get_object_or_404
from post.uploads import S3ImgUploader
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Profile, Follower
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, ProfileSerializer, ChangePasswordSerializer, FollowerSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_otp, send_otp_via_email
import requests


# 회원가입
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

# 회원탈퇴
class Withdrawal(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user = request.user
        provided_password = request.data.get('password', None)
        if not provided_password or not check_password(provided_password, user.password):
            return Response({"error":"비밀번호가 정확하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = RefreshToken.for_user(user)
        refresh_token.blacklist()

        profile = user.profile
        profile.name = f'deleteuser_{profile.id}'
        profile.save()

        user.is_active = False
        user.save()

        return Response({"message":"회원탈퇴 되었습니다."}, status=status.HTTP_200_OK)


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
    

# 이메일 인증
class GenerateOtp(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error':'이메일 주소를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.filter(email__iexact=email)
        if not users.exists():
            otp = generate_otp()
            send_otp_via_email(email, otp=otp)
            response = {'message':'인증 번호 생성', 'otp':otp}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response({'error': '이미 가입된 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 변경
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def put (self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response({"error":"현재 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()

            return Response({"messsge":"비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)



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
            "profile": profile_data
        }

        return Response(data, status=status.HTTP_200_OK)


# 프로필 수정
class ProfileEdit(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data)

        if 'image' in request.FILES:
            image_file = request.FILES['image']
            uploader = S3ImgUploader(image_file)
            image_url = uploader.upload('profile')
            profile.image = image_url
            profile.save()

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필 수정 완료"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# 팔로우
class Follow(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)
        if request.user == target_user:
            return Response({"error" : "본인을 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        _,created = Follower.objects.get_or_create(target_id=target_user, follower_id=request.user)
        if created:
            return Response({"message":"팔로우 성공"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"이미 팔로우한 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)
        

# 언팔로우
class UnFollow(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)
        follow_reaction = get_object_or_404(Follower, target_id=target_user, follower_id=request.user)
        follow_reaction.delete()
        return Response({"message":"언팔로우 성공"}, status=status.HTTP_204_NO_CONTENT)
    

# 팔로우 목록 조회
class FollowerList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        followers = [follower.follower_id for follower in user.followers.all()]
        serializer = FollowerSerializer(followers, many=True, context={'request' : request})
        return Response({'follower_list' : serializer.data}, status=status.HTTP_200_OK)