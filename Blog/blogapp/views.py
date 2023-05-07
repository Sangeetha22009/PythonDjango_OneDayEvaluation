from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, BlogForm, BlogPostForm
from .models import Blog, BlogPost, Comment, Share
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def index(request):
    return render(request, "blogapp/index.html")

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
        return render(request, "blogapp/login.html")

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
    return render(request, "blogapp/register.html", {'registraion_form': registraion_form})

@login_required(login_url='login')
def create_blog(request):    
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            breakpoint()
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                image = form.cleaned_data['cover_image']
                blog = Blog(
                    title=title, description=description, cover_image = image, created_by = request.user )                
                blog.save()
                messages.success(request, 'Blog created successfully!!')                
                return redirect('/')
            else:
                messages.error(request, 'Error occured while creating blog!!')
        else:            
            return render(request, 'blogapp/create-blog.html')    
        