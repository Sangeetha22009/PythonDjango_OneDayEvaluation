from django.urls import path
from . import views

urlpatterns = [    
    path("", views.index, name = "index" ),
    path("register", views.register, name = "register" ),
    path('image-upload/',views.image_upload, name='image-upload')
]