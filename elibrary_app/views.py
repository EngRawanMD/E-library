from dataclasses import dataclass
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import BookForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')
    username = None
    password = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'Login failed! , try again!')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'User or password does not match!')

    context = {'page': page}
    return render(request, 'pages/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    return render(request, 'pages/login_register.html',{'form': form})




@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        add_book = BookForm(request.POST,request.FILES)
        if add_book.is_valid():
            add_book.save()

        add_category = CategoryForm(request.POST)
        if add_category.is_valid():
            add_category.save()

    context = {
        'category':Category.objects.all(),
        'books':Book.objects.all(),
        'form': BookForm(),
        'formcat': CategoryForm(),
        'allbooks': Book.objects.filter(active=True).count(),
        'booksold': Book.objects.filter(state='sold').count(),
        'bookrental': Book.objects.filter(state='rental').count(),
        'bookavaliable': Book.objects.filter(state='avaliable').count(),
    }
    return render(request, 'pages/index.html', context)


def books(request):
    search = Book.objects.all()
    title = None
    if 'search_name' in request.GET:
        title = request.GET['search_name']
        if title:
            search = search.filter(title__icontains = title)

    context = {
        'category':Category.objects.all(),
        'books':search,
        'formcat': CategoryForm(),
    }
    return render(request, 'pages/books.html', context)

@login_required(login_url='login')
def update(request, id):
    book_id = Book.objects.get(id=id)
    if request.method == 'POST':
        book_update = BookForm(request.POST, request.FILES, instance=book_id)
        if book_update.is_valid():
            book_update.save()
            return redirect('/')

    else:
        book_update = BookForm(instance=book_id)

    context = {
        'form':book_update,
    }    
    return render(request, 'pages/update.html', context)

@login_required(login_url='login')
def delete(request, id):
    book_delete = get_object_or_404(Book,id=id)
    if request.method == "POST":
        book_delete.delete()
        return redirect('/')
    return render(request, 'pages/delete.html')    




