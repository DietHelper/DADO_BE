from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', through='Like')
    
    def __int__(self):
        return self.id

    class Meta:
        db_table = 'post'


class PostImage(models.Model):
    id = models.AutoField(primary_key=True)
<<<<<<< HEAD
<<<<<<< HEAD
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', null=True)
    image = models.CharField(max_length=100)
=======
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
=======
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', null=True)
>>>>>>> 618a96b (feat : s3 연동 설정 및 다중 이미지 글 생성 기능 추가)
    image = models.FileField()
>>>>>>> 636c424 (feat : s3 연동 설정 및 uploads.py 코드 추가)

    def __int__(self):
        return self.id
    

    class Meta:
        db_table = 'post_image'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)