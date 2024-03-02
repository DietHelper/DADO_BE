from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.PostIndex.as_view(), name='index'),
    path('postcreate/', views.PostCreate.as_view(), name='post_create'),
    path('image/', views.PostImage.as_view(), name='image'),
]
