from django.urls import path
from .views import Join, Login, Logout, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('join/', Join.as_view(), name='join'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path("profile/", ProfileView.as_view(), name='profile'),
]

