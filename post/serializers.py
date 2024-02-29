from rest_framework import serializers
from .models import Post, Comment, PostImage

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    
    def get_images(self, obj):
        image = obj.image_set.all()
        return PostImageSerializer(instance=image, many=True, context=self.context).data
    
    class Meta:
        model = Post
        exclude = ['writer']
    
    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        instance = Post.objects.create(**validated_data)
        
        for image_data in images_data:
            PostImage.objects.create(post=instance, image=image_data)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
