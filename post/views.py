from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, PostImage
from .serializers import PostSerializer, CommentSerializer, PostImageSerializer
from django.shortcuts import render
from dotenv import load_dotenv
import boto3
import uuid
import os
from django.http import JsonResponse
from .uploads import S3ImgUploader
import json

User = get_user_model()

class PostIndex(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

# 한개의 이미지만 s3에 올리기 성공
class PostImage(APIView):
    def post(self, request, format=None):
        serializer = PostImageSerializer(data=request.data)
        if serializer.is_valid():
            image_file = request.data.get('image')
            s3_uploader = S3ImgUploader(image_file)
            folder = 'post_image'
            url = s3_uploader.upload(folder)
            serializer.save(image=url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCreate(APIView):
    def post(self, request):
        user = request.user
        post_data = {
            'title': request.data['title'],
            'content': request.data['content'],
            'writer': user
        }
        images = request.FILES.getlist('image')
        print(images)
        post = Post.objects.create(**post_data)
        print(post)
        for image in images:
            img_uploader = S3ImgUploader(image)
            folder = 'post_image'
            uploaded_url = img_uploader.upload(folder)

            PostImage.objects.create(post=post,image=uploaded_url)
            
        data = {
            "message" : "글 생성 완료 "
        }
        return Response(data, status=status.HTTP_201_CREATED)
