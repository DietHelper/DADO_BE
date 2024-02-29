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

User = get_user_model()

class Index(APIView):
    def get(self, request):
        post = Post.objects.all()
        serializer = PostSerializer(post)
        return Response(serializer.data)
        

    
