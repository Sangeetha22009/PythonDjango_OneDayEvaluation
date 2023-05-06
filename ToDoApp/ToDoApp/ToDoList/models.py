from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoList(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    