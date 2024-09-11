from rest_framework import serializers
from .models import Crew, Tag

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'

class TagSeirializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'