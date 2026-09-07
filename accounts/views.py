from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def logout_page(request):
    logout(request)
    return redirect('home')

def login_page(request):
    form = AuthenticationForm()
    page = 'login'
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')

    context = {'form': form, 'page': page}
    return render(request, 'accounts/login_register.html', context)

def register_page(request):
    form = RegisterForm()
    page = 'register'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    context = {'form': form, 'page': page}
    return render(request, 'accounts/login_register.html', context)