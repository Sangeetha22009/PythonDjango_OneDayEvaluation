from django.contrib import admin

# Register your models here.
from .models import ToDoItem, ToDoList

#register sites here

class ToDoListAdmin(admin.ModelAdmin):
    list_display = ['title','description','created_at']

    
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = ['title','description','due_date','is_completed','created_at','todo_list']

admin.site.register(ToDoList, ToDoListAdmin)
admin.site.register(ToDoItem, ToDoItemAdmin)