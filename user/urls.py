from django.urls import path
from .views import Join, Login
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('join/', Join.as_view(), name='join'),
    path('login/', Login.as_view(), name='login'),
]

