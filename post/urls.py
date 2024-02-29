from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('index/', views.PostIndex.as_view(), name='index'),
    path('postcreate/', views.PostCreate.as_view(), name='post_create'),
=======
    path('index/', views.Index.as_view(), name='index'),
    path('postwrite/', views.PostWrite.as_view(), name='postwrite'),
    path('upload/', views.PostImage.as_view(), name='upload'),
>>>>>>> 636c424 (feat : s3 연동 설정 및 uploads.py 코드 추가)
]
