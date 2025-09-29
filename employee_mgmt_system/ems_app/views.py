from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# ...existing code...

@login_required
def employee_profile(request):
    error = None
    success = None
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                error = "Passwords do not match."
            elif new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                success = "Password updated successfully."
        if not error:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            if not success:
                success = "Profile updated successfully."
    return render(request, "employee/profile.html", {"error": error, "success": success})
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.is_superuser:  # Admin login
                return redirect("admin_dashboard")
            else:  # Employee login
                return redirect("employee_dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("home")

    return render(request, 'signin.html')

def employee_dashboard(request):
    return render(request, 'employee/index.html')


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in user after signup
            return redirect("home")  # Redirect to homepage
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})