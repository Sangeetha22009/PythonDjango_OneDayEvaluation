from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, ToDoListForm, ToDoItemForm
from .models import ToDoList, ToDoItem
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
import json

# Create your views here.
render_items_html =  "ToDoList/todo-items.html" 
render_list_html =  "ToDoList/todo-list.html" 

@login_required(login_url='login')
def edit_item(request, item_id):
    breakpoint()
    item = ToDoItem.objects.get(id=item_id)
    todo_list_id = item.todo_list.id
    return redirect('todo-item/' + str(todo_list_id))

@login_required(login_url='login')
def delete_item(request):
    body = json.loads(request.body)
    todo_item_id = body['todo_item_id']
    item = ToDoItem.objects.filter(id=todo_item_id)                
    if item is not None:
        item.delete()
        return JsonResponse({
            'is_deleted' : True
        })
    else:
        messages.error(request, 'Item not found')
        return render(request, render_items_html)
     
@login_required(login_url='login')
def todo_item(request, todo_list_id, todo_item_id=None):   
    if request.method == 'POST':
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            todolist = ToDoList.objects.get(id=todo_list_id)
            due_date = form.cleaned_data['due_date']
            is_completed = form.cleaned_data['is_completed']
            if todo_item_id is not None:
                item_obj = ToDoItem.objects.get(id=todo_item_id)
                item_obj.title = title
                item_obj.description = description
                item_obj.due_date = due_date
                item_obj.is_completed = is_completed
                item_obj.save()
                messages.success(request, 'Item Updated Successfully !!')
            else:
                item = ToDoItem( todo_list = todolist, title = title, description=description, due_date= due_date,  is_completed = is_completed)
                item.save()
                messages.success(request, 'Item added succesfully !')
            items = ToDoItem.objects.all().order_by('-id').filter(todo_list__id = todo_list_id)
            context = {
                'items' : items,
                'todo_list_id': todo_list_id
            }
            return render(request, render_items_html, context)
        else:
            messages.error(request, 'Invalid form, please check and update')
        return render(request, render_items_html)
    else:                
        list_edit_item = ToDoItem()
        if todo_item_id is not None:
            list_edit_item = ToDoItem.objects.get(Q(id = todo_item_id))            
        items = ToDoItem.objects.all().order_by('-id').filter(todo_list__id = todo_list_id)
        form = ToDoItemForm()
        context = {
            'form': form,
            'items': items,
            'todo_list_id': todo_list_id,
            'list_edit_item': list_edit_item
        } 
        return render(request, render_items_html, context)

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

@login_required(login_url='login')
def todo_list(request):
        if request.method == 'POST':
            form = ToDoListForm(request.POST, auto_id=True)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                id = request.POST.get('id')
                if id is not None:
                    list_obj = ToDoList.objects.get(id=id)
                    list_obj.title = title
                    list_obj.description = description
                    list_obj.save()
                    messages.success(request, 'List Updated Successfully !!')
                else: 
                    list_obj = ToDoList(
                        title=title, description=description, created_by = request.user )
                    list_obj.save()
                    messages.success(request, 'List Created Successfully !!')
            else:
                messages.error(request, 'Error occured while saving')

        listobj = ToDoList.objects.all().order_by('-id') .filter(Q(created_by = request.user))
        count = listobj.count
        context = {
            'listobj' : listobj,
            'count': count
        }
        return render(request, render_list_html, context)

@login_required(login_url='login')
def delete_list(request, list_id):
    list = ToDoList.objects.filter(id=list_id)                
    if list is not None:
        list.delete()
        listobj = ToDoList.objects.all().order_by('-id') .filter(Q(created_by = request.user))
        count = listobj.count
        context = {
            'listobj' : listobj,
            'count': count
        }
        messages.success(request, 'Todo list record deleted successfully !')
        return render(request, render_list_html, context)
    else:
        messages.error(request, 'Item not found')
        return render(request, render_items_html)

@login_required(login_url='login')
def edit_list(request, list_id):
    list = ToDoList.objects.get(id=list_id)                
    listobj = ToDoList.objects.all().order_by('-id') .filter(Q(created_by = request.user))
    count = listobj.count
    context = {
        'listobj' : listobj,
        'count': count,
        'item': list,
        'is_edit':True
    }
    return render(request, render_list_html, context)


@login_required(login_url='login')
def grid_content(request):
    listobj = ToDoList.objects.all().order_by('-id') .filter(Q(created_by = request.user))
    count = listobj.count
    context = {
        'listobj' : listobj,
        'count': count
    }
    return render(request, 'ToDoList/partials/_grid.html', context)