from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

class User(BaseModel):
    name = models.CharField(max_length=50)
    passwd = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    img = models.CharField(max_length=255)

class BlogInfo(BaseModel):
    title = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    comment_count = models.IntegerField(default=0)
    cover_img = models.CharField(max_length=255)
    favor_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)

class BlogComment(BaseModel):
    blog_info_id = models.ForeignKey(BlogInfo, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User)
    content = models.TextField()