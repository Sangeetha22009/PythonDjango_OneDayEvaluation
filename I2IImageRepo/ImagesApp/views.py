from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageUploadForm, UserRegistrationForm
from .models import Gallery
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    return render(request, "ImagesApp/index.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)                
                return redirect('/')
            else:
                messages.error(request, "Inavlid User Name or Password")
        return render(request, "ImagesApp/login.html")

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def register(request):
    registraion_form = UserRegistrationForm()
    if request.method == 'POST':
        registraion_form = UserRegistrationForm(request.POST)
        if registraion_form.is_valid():
            registraion_form.save()
            messages.success(request, 'Registered Successfuly, Please Login..')
            return redirect('/login')
    return render(request, "ImagesApp/register.html", {'registraion_form': registraion_form})


def image_details(request, image_id):
    print('image-details')
    image = Gallery.objects.get(id=image_id)
    return render(request, 'ImagesApp/image-details.html' , {'image': image}) 

def gallery(request):
    searchText = '' 
    if request.GET.get('search_text') is not None:
        searchText = request.GET.get('search_text')   
    images = Gallery.objects.all().order_by('-id') \
            .filter(Q(title__icontains = searchText) | Q(description__icontains = searchText) | Q(category__icontains = searchText))
    paginator  = Paginator(images, 4)
    current_page = request.GET.get('page')
    paginated_images = paginator.get_page(current_page)
    count = images.count
    context = {
        'images' : paginated_images,
        'count': count
    }
    return render(request, 'ImagesApp/gallery.html', context)

# image-upload
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        # breakpoint()
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']

            # save image to server
            image_obj = Gallery(
                title=title, description=description, image=image, category=category, uploaded_by = request.user.username )
            image_obj.save()
            return redirect('gallery')
            # redirect to success html or gallery page
            return HttpResponse('Saved successfully')
        else:
            raise Exception('Error occured ', form.errors)
            # need to add messages to display errors
            return render(request, 'ImagesApp/image-upload.html')
    else:
        form = ImageUploadForm()
        context = {
            'form': form
        }
        return render(request, 'ImagesApp/image-upload.html', context)
