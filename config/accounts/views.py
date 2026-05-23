from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

User = get_user_model()


# 🔹 REGISTER VIEW
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register_user")

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register_user")

        user = User.objects.create_user(
            email=email,
            password=password,
            username=username,
            role=role
        )

        messages.success(request, "Account created successfully.")
        return redirect("login_user")

    return render(request, "accounts/register.html")


# 🔹 LOGIN VIEW (Email Based)
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login_user")

    return render(request, "accounts/login.html")


# 🔹 LOGOUT VIEW
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")