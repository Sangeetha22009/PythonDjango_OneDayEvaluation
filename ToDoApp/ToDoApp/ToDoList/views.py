from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, ToDoListForm
from .models import ToDoList
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def todo_item(request, todolist_id):
    return render(request, "ToDoList/todo-items.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/todo-list')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)                
                return render(request, 'ToDoList/todo-list.html')
            else:
                messages.error(request, "Inavlid User Name or Password")
        return render(request, "ToDoList/login.html")

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
    return render(request, "ToDoList/register.html", {'registraion_form': registraion_form})


def todo_list(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ToDoListForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']

                list_obj = ToDoList(
                    title=title, description=description, created_by = request.user.username )
                list_obj.save()
                messages.success(request, 'List Created Successfully !!')
                
                listobj = ToDoList.objects.all().order_by('-id').filter(Q(created_by = request.user.username))
                paginator  = Paginator(listobj, 4)
                current_page = request.GET.get('page')
                paginated_list = paginator.get_page(current_page)
                count = listobj.count
                context = {
                    'listobj' : paginated_list,
                    'count': count
                }
                return render(request, 'ToDoList/todo-list.html', context)
                
    return render(request, "ToDoList/todo-list.html")

