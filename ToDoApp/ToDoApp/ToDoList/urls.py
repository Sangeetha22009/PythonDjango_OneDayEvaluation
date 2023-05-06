from django.urls import path
from . import views

urlpatterns = [    
    path("", views.user_login, name = "login" ),
    path("register", views.register, name = "register" ),
    path("login", views.user_login, name = "login" ),
    path("logout", views.user_logout, name = "logout" ),
    path("todo-item/<int:todolist_id>/", views.todo_item, name='todo-item'),
    path("todo-list", views.todo_list, name = "todo-list" ),
]