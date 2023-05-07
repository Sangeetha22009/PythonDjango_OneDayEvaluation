from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def get_file_name(path, filename=''): 
    date_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'{date_time_now}_{ filename }'
    return os.path.join(path, filename)

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    cover_image = models.ImageField(upload_to= get_file_name(path='uploads/cover_images'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

class BlogPost(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField()
    image = models.ImageField(upload_to= get_file_name(path='uploads/post_images'))
    is_like = models.BooleanField(default=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment = models.TextField()    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    social_media = models.TextField()    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
