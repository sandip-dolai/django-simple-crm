from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()

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
    else:
        return render(request, "web_crm/home.html", {"records": records})


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


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(
            request,
            "web_crm/customer_record.html",
            {"customer_record": customer_record},
        )
    else:
        messages.error(request, "You must be logged in to view customer records.")
        return redirect("home")


def delete_record(request, pk):
    delete_record = Record.objects.get(id=pk)
    delete_record.delete()
    messages.success(request, "Record deleted successfully.")
    return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record added successfully.")
                return redirect("home")
        return render(request, "web_crm/add_record.html", {"form": form})
    else:
        messages.success(request, "You must be logged in to add a record.")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully.")
            return redirect("customer_record", pk=pk)
        return render(request, "web_crm/update_record.html", {"form": form})
    else:
        messages.success(request, "You must be logged in to update a record.")
        return redirect("home")
