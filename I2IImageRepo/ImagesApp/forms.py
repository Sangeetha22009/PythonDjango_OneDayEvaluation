from django import forms
from .models import Gallery
from django.contrib.auth.forms import UserCreationForm
from .models import User

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title','description','image','category']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter User Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Email Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter Password'})) 
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter Confirm Password'}))
    class Meta:
        model=User
        fields = ['username','email','password1','password2']
 