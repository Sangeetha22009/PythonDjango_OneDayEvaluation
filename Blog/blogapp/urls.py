from django.urls import path
from . import views

urlpatterns = [    
    path("", views.index, name = "index" ),
    path("register", views.register, name = "register" ),
    path("login", views.user_login, name = "login" ),
    path("logout", views.user_logout, name = "logout" ),
    path("create-blog",views.create_blog, name = "create-blog"),
    path('view-posts/<int:blog_id>/', views.view_posts, name='view-posts'),
    path('add-edit-post/<int:blog_id>/', views.add_edit_post, name='add-edit-post')
]