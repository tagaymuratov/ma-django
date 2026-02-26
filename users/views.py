from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm  
from .models import CustomUser

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("/")
        else:
            messages.error(request, "Заполните все поля корректно.")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("/")
    else:
        form = CustomUserLoginForm()
    return render(request, "users/login.html", {"form": form})

@login_required(login_url="/users/login")
def profile_view(request):
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return TemplateResponse(request, "users/profile.html", {
        "form": form,
        "user": request.user
    })

@login_required(login_url="/users/login")
def account_details(request):
    user = CustomUser.objects.get(id=request.user.id)
    return TemplateResponse(request, "users/account_details.html", {"user": user})

@login_required(login_url="/users/login")
def edit_account_details(request):
    form= CustomUserUpdateForm(instance=request.user)
    return TemplateResponse(request, "users/edit_account_details.html", {"form": form, "user": request.user})

@login_required(login_url="/users/login")
def update_account_details(request):
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.clean()
            user.save()
            updated_user = CustomUser.objects.get(id=request.user.id)
            request.user = updated_user
            return TemplateResponse(request, "users/account_details.html", {"user": updated_user})
        else:
            return TemplateResponse(request, "users/edit_account_details.html", {"form": form, "user": request.user})
    return redirect('users:profile')

def logout_view(request):
    logout(request)
    return redirect("/")