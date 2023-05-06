from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import Gallery
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, "ImagesApp/index.html" )

def register(request):
    return render(request, "ImagesApp/register.html" )

def gallery(request):
    searchText = '' 
    if request.GET.get('search_text') is not None:
        searchText = request.GET.get('search_text')   
    images = Gallery.objects.all().order_by('-id') \
            .filter(Q(title__icontains = searchText) | Q(description__icontains = searchText) | Q(category__icontains = searchText))
    
    context = {
        'images' : images
    }
    return render(request, 'ImagesApp/gallery.html', context)


#image-upload
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        # breakpoint()
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']

            #save image to server
            image_obj = Gallery(title=title, description=description, image=image, category=category,)
            image_obj.save()
            return redirect('gallery')
            return HttpResponse('Saved successfully') # redirect to success html or gallery page
        else:
            raise Exception('Error occured ', form.errors)
            return render(request, 'ImagesApp/image-upload.html')     # need to add messages to display errors
    else:
        form = ImageUploadForm()
        context = {
            'form', form
        }
        return render(request, 'ImagesApp/image-upload.html')
    
