from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from .models import Blog, BlogPost, Comment,  Share
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url="login")
def index(request):
    print('test' , request.user.id)
    posts = BlogPost.objects.filter(created_by=request.user.id).order_by('-id')
    paginator = Paginator(posts, 5)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paged_posts = paginator.get_page(current_page)
    return render(request, "blogapp/index.html", {'posts':paged_posts, 'count': posts.count })

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