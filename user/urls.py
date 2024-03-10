from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('join/', views.Join.as_view(), name='join'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile-detail'),
    path('profile-edit/', views.ProfileEdit.as_view(), name='profile-edit'),
]

