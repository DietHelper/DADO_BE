from rest_framework import serializers
from .models import User, Profile, Follower



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            password = validated_data['password'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    # is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'image', 'nickname', 'age', 'gender', 'height', 'start_weight', 'goal_weight', 'about', 'email']


class FollowerSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(source='profile.image')
    nickname = serializers.CharField(source='profile.nickname')
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields  =['id', 'profile_image', 'nickname', 'is_following']

    def get_is_following(self, obj):
        #팔로잉 목록
        request_user = self.context['request'].user
        return Follower.objects.filter(follower_id=request_user, target_id=obj).exists()

        
