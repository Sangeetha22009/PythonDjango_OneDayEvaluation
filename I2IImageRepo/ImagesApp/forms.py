from django import forms
from .models import Gallery

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title','description','image','category']
 