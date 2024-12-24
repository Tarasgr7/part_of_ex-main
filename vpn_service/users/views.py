from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm, CustomUserChangeForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to profile after successful login
            else:
                # Handle invalid credentials (optional: display error message)
                pass
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required  # Require user to be logged in to access profile
def profile(request):
    return render(request, 'users/profile.html')  # Simplified profile view

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)  # Update user instance
        if form.is_valid():
            form.save()
            # Handle successful update (optional: display confirmation message)
            return redirect('profile')  # Redirect back to profile after update
    else:
        form = CustomUserChangeForm(instance=request.user)  # Pre-populate the form with user data
    return render(request, 'users/edit_profile.html', {'form': form})  # Pass the form to the template

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout