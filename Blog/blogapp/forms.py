from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Blog, BlogPost

from django.core.exceptions import ValidationError
from PIL import Image
import os
from django.core.files.uploadedfile import InMemoryUploadedFile

def get_file_size(file):
    if isinstance(file, InMemoryUploadedFile):
        # Get the size of the InMemoryUploadedFile
        file_size = file.size
        return file_size
    else:
        # File is not an InMemoryUploadedFile
        return None
    
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter User Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Email Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter Password'})) 
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter Confirm Password'}))
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = ['title', 'description', 'cover_image']
#         cover_image = forms.ImageField(
#         error_messages={
#             'invalid_image': 'Only JPG, JPEG, and PNG files are allowed.',
#         }
#     )

class CustomImageField(forms.ImageField):
    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return None

        try:
            img = Image.open(f)
            # Perform custom image validation
            width, height = img.size
            if width > 1000 or height > 1000:
                raise ValidationError(f'Image dimensions must be within 1000x1000 pixels. uploaded dimensions is: {width}*{height} pixels')
            # Get the file size in bytes
            file_size = get_file_size(f)
            if file_size is not None:
                rounded_file_size = round(file_size/(1024*1024), 2)
            # Perform custom validations based on file size
                if file_size > 2 * 1024 * 1024:  # Example: Check if file size exceeds 10 MB
                    raise ValidationError(f'File size must not exceed 2 MB. uploaded file size is {rounded_file_size} MB')
            
        except (IOError, OSError):
            raise ValidationError(self.error_messages['invalid_image'], code='invalid_image')

        return f

class BlogForm(forms.ModelForm):
    cover_image = CustomImageField(
        error_messages={
            'invalid_image': 'Only JPG, JPEG, PNG related image type files are allowed.',
})
    class Meta:
        model = Blog
        fields = ['title', 'description', 'cover_image']  
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']