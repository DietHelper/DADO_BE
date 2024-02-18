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
    class Meta:
        model = Profile
        fields = ['']