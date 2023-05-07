from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, BlogForm, BlogPostForm
from .models import Blog, BlogPost, Comment,  Share
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url="login")
def index(request):
    keyword = request.GET.get('keyword')    
    if keyword is None:
        keyword = ''
    blogs = Blog.objects.filter(Q(created_by=request.user.id) & (Q(title__icontains=keyword)
                                | Q(description__icontains=keyword))).order_by('-id')
    paginator = Paginator(blogs, 5)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paged_blogs = paginator.get_page(current_page)
    return render(request, "blogapp/index.html", {'blogs':paged_blogs, 'count': blogs.count })

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
                return render(request, 'blogapp/create-blog.html') 
        else:            
            return render(request, 'blogapp/create-blog.html')    


@login_required(login_url='login')
def view_posts(request, blog_id):
    keyword = request.GET.get('keyword')  
    if keyword is None:
        keyword = ''
    posts = BlogPost.objects.filter(Q(blog__id=blog_id) & Q(created_by=request.user.id) & (Q(title__icontains=keyword)
                                | Q(content__icontains=keyword))).order_by('-id')
    paginator = Paginator(posts, 5)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paged_posts = paginator.get_page(current_page)
    return render(request, 'blogapp/view-posts.html', {'blog_id': blog_id, 'posts':paged_posts,  'count': posts.count })