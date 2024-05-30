from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('join/', views.Join.as_view(), name='join'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('withdrawl/', views.Withdrawal.as_view(), name='withdrawl'),
    path('changepassword/', views.ChangePassword.as_view(), name='changepassword'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('otp/', views.GenerateOtp.as_view(), name='otp'),
    # path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile-detail'),
    path('profile-edit/', views.ProfileEdit.as_view(), name='profile-edit'),
    path('<int:user_id>/follow/', views.Follow.as_view(), name='follow'),
    path('<int:user_id>/unfollow/', views.UnFollow.as_view(), name='unfollow'),
]

