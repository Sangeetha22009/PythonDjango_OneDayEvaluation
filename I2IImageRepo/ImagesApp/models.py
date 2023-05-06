from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getfilename(request, filename): 
    date_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'{date_time_now}_{ filename }'
    return os.path.join('uploads/images', filename)

# Create your models here.
class Gallery(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to=getfilename,blank=False, null=False)
    description = models.CharField(max_length=200,blank=False, null=False)
    category = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self) -> str:
        return {self.title, self.image}
    