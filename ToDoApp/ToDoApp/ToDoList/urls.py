from django.urls import path
from . import views

urlpatterns = [    
    path("", views.user_login, name = "login" ),
    path("register", views.register, name = "register" ),
    path("login", views.user_login, name = "login" ),
    path("logout", views.user_logout, name = "logout" ),
    path("todo-item/<int:todolist_id>/", views.todo_item, name='todo-item'),
    path("todo-list", views.todo_list, name = "todo-list" ),
    path("delete-item/", views.delete_item, name="delete-item"),
    path("edit-item/<int:todo_item_id>/<int:todo_list_id>/", views.delete_item, name="edit-item"),
    path('delete-list/<int:list_id>/', views.delete_list, name="delete-list"),
    path('edit-list/<int:list_id>/', views.edit_list, name="edit-list")
]