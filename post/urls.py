from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('index/', views.PostIndex.as_view(), name='index'),
    path('postcreate/', views.PostCreate.as_view(), name='post_create'),
    path('postedit/<int:pk>/', views.PostEdit.as_view(), name='post_edit'),
]
