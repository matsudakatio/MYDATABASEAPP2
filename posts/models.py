from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """投稿モデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField("タイトル", max_length=100)
    content = models.TextField("内容", blank=True, null=True)
    image = models.ImageField("画像", upload_to='images/')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return self.title

    # いいねの数を返すプロパティ
    @property
    def total_likes(self):
        return self.likes.count()