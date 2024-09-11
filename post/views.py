from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, PostImage, Like
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCreate(APIView):
    permission_classes = [IsAuthenticated]
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
    

class PostEdit(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        post = Post.objects.get(id=pk)

        post.title = request.data.get('title', post.title)
        post.content = request.data.get('content', post.content)
        post.save()

        img_edit = request.data.get('img_edit')

        if img_edit == 'true':
            prev_img = PostImage.objects.filter(post-post)
            prev_img.delete()

            images = request.FILES.getlist('images')

            for image in images:
                img_uploader = S3ImgUploader(image)
                uploaded_url = img_uploader.upload()
                PostImage.objects.create(post=post, image=uploaded_url)

        data = {
            "message" : "글 수정 완료"
        }
        return Response(data, status=status.HTTP_200_OK)
    

class PostDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        user = request.user
        try: 
            post = Post.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404
        
        images = post.image.all()

        for image in images:
            image.image.delete()
            image.delete()

        post.is_active = False
        post.save()

        return Response({"message":"게시물 삭제 완료"}, status=status.HTTP_200_OK)
    

class PostLike(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # post_id = request.data.get('post_id')
        user = request.user

        # post = get_object_or_404(Post, pk=post_id)
        # like, created = Like.objects.get_or_create(post=post, user=user)
        try:
            post = Post.objects.get(id=request.data['post_id'])
            like, created = Like.objects.get_or_create(post=post, user=user)
        except:
            return Response({"error" : "잘못된 접근입니다."}, status=status.HTTP_404_NOT_FOUND)

        if created:
            return Response({"message" : "좋아요 성공"}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({"message" : "좋아요 취소"}, status=status.HTTP_200_OK)

