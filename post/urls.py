from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    path('postwrite/', views.PostCreate.as_view(), name='postwrite'),
    path('upload/', views.PostImage.as_view(), name='upload'),
]
