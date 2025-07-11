from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm


def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home")
        else:
            messages.success(request, "Invalid username or password")
            return redirect("home")
    return render(request, "web_crm/home.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful")
                return redirect("home")
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
            return render(request, "web_crm/register.html", {"form": form})
    else:
        form = SignUpForm()
    return render(request, "web_crm/register.html", {"form": form})
