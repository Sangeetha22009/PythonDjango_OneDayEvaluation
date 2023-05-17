import base64
from sqlite3 import Blob
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse

#external libraries
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

#application libraries
from .forms import UserRegistrationForm, BlogForm, BlogPostForm
from .models import Blog, BlogPost, Comment,  Share

# Create your views here.
@login_required(login_url="login")
def index(request):
    search_keyword = request.GET.get('keyword', '')
    blogs = Blog.objects.filter(Q(created_by=request.user.id) & (Q(title__icontains=search_keyword)
                                | Q(description__icontains=search_keyword))).order_by('-id')
    paginator = Paginator(blogs, 5)
    current_page = request.GET.get('page') or 1
    paged_blogs = paginator.get_page(current_page)
    return render(request, "blogapp/index.html", {'blogs': paged_blogs, 'count': blogs.count()})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "blogapp/login.html", {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    return redirect('/')

def register(request):
    registration_form = UserRegistrationForm()
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            messages.success(request, 'Registered Successfuly, Please Login..')
            return redirect('/login')
    return render(request, "blogapp/register.html", {'registraion_form': registration_form})

@login_required(login_url='login')
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                image = form.cleaned_data['cover_image']
                thumbnail_image = request.FILES.get('thumbnail_image')
                if thumbnail_image:
                    thumbnail_bytes =  thumbnail_image.read()
                    # thumbnail_bytes = thumbnail_image.read() # read image data 
                    # file_obj = BytesIO(thumbnail_bytes)
                    # file_obj.name = thumbnail_image.name
                    # #create an InMemoryUploadedFile instance
                    # uploaded_file =  InMemoryUploadedFile(
                    #     file = file_obj,
                    #     field_name = 'thumbnail_image', # Field name of the BinaryField
                    #     name = file_obj.name,
                    #     content_type = thumbnail_image.content_type,
                    #     size = thumbnail_image.__sizeof__(),
                    #     charset = None
                    # )
                    blog = Blog(title=title, description=description, cover_image=image, 
                                created_by=request.user, thumbnail_image = thumbnail_bytes)
                else:
                    blog = Blog(title=title, description=description, cover_image=image, 
                                created_by=request.user)
                blog.save()
                messages.success(request, 'Blog created successfully!!', extra_tags='message-success')
                return redirect('/')
            else:
                messages.error(request, 'please find the below validation errors', extra_tags='message-error')
                return render(request, 'blogapp/create-blog.html', {'form': form})
        except Exception as ex:
            messages.error(request, 'Error occured while creating blog!!', extra_tags='message-error')
            return render(request, 'blogapp/create-blog.html')
    return render(request, 'blogapp/create-blog.html')


@login_required(login_url='login')
def view_posts(request, blog_id):
    post_search_keyword = request.GET.get('keyword', '')
    posts = BlogPost.objects.select_related('blog').filter(Q(blog__id=blog_id) & Q(created_by=request.user.id) & (Q(title__icontains=post_search_keyword)
                                                                                                   | Q(content__icontains=post_search_keyword))).order_by('-id')
    paginator = Paginator(posts, 5)
    current_page = request.GET.get('page', 1)
    paged_posts = paginator.get_page(current_page)
    return render(request, 'blogapp/view-posts.html', {'blog_id': blog_id, 'posts': paged_posts,  'count': posts.count})


@login_required(login_url='login')
def add_edit_post(request, blog_id, post_id=None):
    render_html = 'blogapp/add-edit-post.html'
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            if post_id is None:
                post_id = request.POST.get('post_id')
            blog = Blog.objects.get(id=blog_id)
            if post_id is not None:
                blog_post = BlogPost.objects.get(id=post_id)
                blog_post.blog = blog
                blog_post.title = title
                blog_post.content = content
                blog_post.save()
                messages.success(request, 'Blog Post Updated Successfully !!')
            else:
                blog_post = BlogPost(
                    title=title, content=content, image=image, created_by=request.user, blog=blog)
                blog_post.save()
                messages.success(request, 'Blog post created successfully!!')
            url = reverse('view-posts', args=[str(blog_id)])
            return redirect(url)
        else:
            messages.error(
                request, r'Error occured while creating\updating blog post!!')
            return render(request, render_html, {'blog_id': blog_id})
    else:
        if post_id is not None:
            post = BlogPost.objects.get(id=post_id)
            postobj = BlogPost.objects.all().order_by(
                '-id') .filter(Q(created_by=request.user))
            count = postobj.count
            context = {
                'count': count,
                'item': post,
                'is_edit': True,
                'blog_id': blog_id
            }
            return render(request, render_html , context)
        else:
            return render(request, render_html, {'blog_id': blog_id})


@login_required(login_url='login')
def post_comments(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = Comment.objects.filter(post=post).select_related('created_by')

    if request.method == "POST":
        comment = request.POST.get('comment')
        comment = Comment(comment=comment, post=post, created_by=request.user)
        comment.save()

    return render(request, "blogapp/post-comments.html", {'post': post, 'comments': comments})


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    blog_id = post.blog.id

    if post:
        post.delete()
        messages.success(request, 'Post deleted successfully !')
    url = reverse('view-posts', args=[str(blog_id)])
    return redirect(url)


@login_required(login_url='login')
def like_post(request, post_id, is_like):
    post = get_object_or_404(BlogPost, id=post_id)
    blog_id = post.blog.id
    if post:
        post.is_like = is_like
        post.save()

        if is_like:
            messages.success(request, 'Post liked successfully!')
        else:
            messages.success(request, 'Post disliked successfully!')

    url = reverse('view-posts', args=[str(blog_id)])
    return redirect(url)


@login_required(login_url='login')
def share_post(request, post_id, shared_to):
    post = get_object_or_404(BlogPost, id=post_id)
    blog_id = post.blog.id

    allowed_social_media = ['Facebook', 'Twitter']

    if shared_to in allowed_social_media and post:
        share = Share(post=post, social_media=shared_to,
                      created_by=request.user)
        share.save()
        messages.success(request, f'Post shared to {shared_to} successfully!')

    url = reverse('view-posts', args=[str(blog_id)])
    return redirect(url)


@login_required(login_url='login')
def read_more_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    posts = blog.blogpost_set.all()
    BlogPost.objects.all().filter(blog_id = blog_id)
    image_base64 = base64.b64encode(blog.thumbnail_image).decode('utf-8')
    blog.thumbnail_image = image_base64
    context = {
        'posts': posts,
        'blog': blog,      
    }
    return render(request, 'blogapp/read-more-blog.html', context)
