from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    path('index/', views.PostIndex.as_view(), name='index'),
    path('postcreate/', views.PostCreate.as_view(), name='post_create'),
=======
    path('index/', views.Index.as_view(), name='index'),
    path('postwrite/', views.PostWrite.as_view(), name='postwrite'),
    path('upload/', views.PostImage.as_view(), name='upload'),
>>>>>>> 636c424 (feat : s3 연동 설정 및 uploads.py 코드 추가)
=======
    path('index/', views.PostIndex.as_view(), name='index'),
    path('postcreate/', views.PostCreate.as_view(), name='post_create'),
<<<<<<< HEAD
    path('image/', views.PostImage.as_view(), name='image'),
>>>>>>> 618a96b (feat : s3 연동 설정 및 다중 이미지 글 생성 기능 추가)
=======
>>>>>>> 1367670 (chore : 다중 이미지 글 생성 기능 수정)
=======
    path('index/', views.Index.as_view(), name='index'),
    path('postwrite/', views.PostWrite.as_view(), name='postwrite'),
    path('upload/', views.PostImage.as_view(), name='upload'),
>>>>>>> b6eb8a9 (feat : s3 연동 설정 및 uploads.py 코드 추가)
]
