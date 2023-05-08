from django.urls import path
from . import views

urlpatterns = [    
    path("", views.index, name = "index" ),
    path("register", views.register, name = "register" ),
    path("login", views.user_login, name = "login" ),
    path("logout", views.user_logout, name = "logout" ),
    path("create-blog",views.create_blog, name = "create-blog"),
    path('view-posts/<int:blog_id>/', views.view_posts, name='view-posts'),
    path('add-edit-post/<int:blog_id>/<int:post_id>/', views.add_edit_post, name='add-edit-post'),
    path('add-edit-post/<int:blog_id>/', views.add_edit_post, name='add-edit-post'),
    path('delete-post/<int:post_id>/', views.delete_post, name="delete-post"),
    path('like-post/<int:post_id>/<int:is_like>', views.like_post, name="like-post"),
    path('post-comments/<int:post_id>/', views.post_comments, name='post-comments'),
    path('share-post/<int:post_id>/<str:shared_to>', views.share_post, name="share-post"),
    path('read-more/<int:blog_id>/', views.read_more_blog, name='read-more-blog')
]