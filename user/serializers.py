from rest_framework import serializers
from .models import User, Profile



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
    


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    # is_following = serializers.SerializerMethodField() 질문
    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'age', 'gneder', 'height', 'start_weight', 'goal_weight', 'about']



        
