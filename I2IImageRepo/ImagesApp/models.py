from django.db import models

# Create your models here.
class Gallery(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    image_field = models.ImageField(upload_to="uploads/images",blank=False, null=False)
    description = models.CharField(max_length=200,blank=False, null=False)
    category = models.CharField(max_length=50, blank=False, null=False)
    