from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "ImagesApp/index.html" )

def register(request):
    return render(request, "ImagesApp/register.html" )

#image-upload
def image_upload(request):
    return render(request, 'ImagesApp/image-upload.html')
    
