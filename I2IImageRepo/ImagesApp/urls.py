from django.urls import path
from . import views

urlpatterns = [    
    path("", views.index, name = "index" ),
    path("register", views.register, name = "register" ),
    path("login", views.user_login, name = "login" ),
    path("logout", views.user_logout, name = "logout" ),
    path('image-upload/',views.image_upload, name='image-upload'),
    path('gallery/', views.gallery, name='gallery'),
    path('image-details/<int:image_id>/', views.image_details, name='image-details')
]