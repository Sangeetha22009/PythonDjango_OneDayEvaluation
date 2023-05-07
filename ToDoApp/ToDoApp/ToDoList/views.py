from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, ToDoListForm, ToDoItemForm
from .models import ToDoList, ToDoItem
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url='login')
def edit_item(request, item_id, todo_list_id):
    return redirect('todo-item/' + str(todo_list_id))

@login_required(login_url='login')
def delete_item(request, todo_item_id, todo_list_id):
    # prompt = input('are you sure want to delete?')
    # if prompt == 'yes':
        item = ToDoItem.objects.filter(id=todo_item_id)
        if item is not None:
            item.delete()
            items = ToDoItem.objects.all().order_by('-id').filter(todo_list__id = todo_list_id)
            form = ToDoItemForm()
            context = {
                'form': form,
                'items': items,
                'todolist_id': todo_list_id
            } 
            return render(request, "ToDoList/todo-items.html", context)
        else:
            messages.error(request, 'Item not found')
            return redirect('/todo-item/' + str(todo_list_id))
    # else:
    #     return redirect('/todo-item/' + str(todo_list_id))

        

@login_required(login_url='login')
def todo_item(request, todolist_id):
    if request.method == 'POST':
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            todolist = ToDoList.objects.get(id=todolist_id)
            due_date = form.cleaned_data['due_date']
            is_completed = form.cleaned_data['is_completed']
            item = ToDoItem( todo_list = todolist, title = title, description=description, due_date= due_date,  is_completed = is_completed)
            item.save()
            messages.success(request, 'Item added succesfully !')
            items = ToDoItem.objects.all().order_by('-id').filter(todo_list__id = todolist_id)
            context = {
                'items' : items,
                'todolist_id': todolist_id
            }
            return render(request, "ToDoList/todo-items.html" , context)
        else:
            messages.error(request, 'Invalid form, please check and update')
        return render(request, "ToDoList/todo-items.html")
    else:
        items = ToDoItem.objects.all().order_by('-id').filter(todo_list__id = todolist_id)
        # paginator = Paginator(items, 5)
        # current_page = request.GET.get('page')
        # paged_items = paginator.get_page(current_page)
        form = ToDoItemForm()
        context = {
            'form': form,
            'items': items,
            'todolist_id': todolist_id
        } 
        return render(request, "ToDoList/todo-items.html", context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('todo-list')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)                
                return redirect('todo-list')
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
                    title=title, description=description, created_by = request.user )
                list_obj.save()
                messages.success(request, 'List Created Successfully !!')
                
                listobj = ToDoList.objects.all().order_by('-id').filter(Q(created_by = request.user))
                count = listobj.count
                context = {
                    'listobj' : listobj,
                    'count': count
                }
                return render(request, 'ToDoList/todo-list.html', context)
            else:
                messages.error(request, 'Error occured while saving')
        else:
            listobj = ToDoList.objects.all().order_by('-id') .filter(Q(created_by = request.user))
            count = listobj.count
            context = {
                'listobj' : listobj,
                'count': count
            }
            return render(request, 'ToDoList/todo-list.html', context)
    return redirect('login')

