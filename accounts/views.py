from accounts.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegister, AccountUpdateForm, ProfileUpdateForm
from .decorators import unauthenticated_user
from django.core.mail import send_mail


# User registeration view
@unauthenticated_user
def signup_view(request):
    template_name = "accounts/signup.html"
    if request.method == 'POST':
        signup_form = UserRegister(request.POST)
        if signup_form.is_valid():
            users = signup_form.save(commit=False)
            users.save()
            for user in User.objects.all():
                Profile.objects.get_or_create(user=user)
            messages.success(request, f"Your account has successfully been created, you can now log in".capitalize())
            return redirect('account-login')
        else:
            messages.warning(request, f"Some of your information are either existing or not matching, try again")
            return redirect('account-signup')
    else:
        template_name = "accounts/signup.html"
    signup_form = UserRegister()
    context = {"signup_form": signup_form}
    return render(request, template_name, context)


#User login
@unauthenticated_user
def login_view(request):
    template_name = "accounts/login.html"
    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f"welcome {user}, you are now logged in".capitalize())
            return redirect("budget_list")
        else:
            messages.warning(request, f"Invalid username or password")
            return redirect('account-login')
    else:
        template_name = "accounts/login.html"
    login_form = AuthenticationForm()
    context = {"login_form": login_form}
    return render(request, template_name, context)
    

# user logout
def logout_view(request):
    if request.method == 'POST':
        template_name= "accounts/logout.html"
        logout(request)
        return render(request, template_name)


# Update Profile
@login_required(login_url="account-login")
def profile_update_view(request, pk):
    template_name = "accounts/user_profile.html"
    user_update_form = None
    image_update_form = None
    user = get_object_or_404(User,pk=pk)
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        user_update_form = AccountUpdateForm(request.POST, instance=user)
        image_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_update_form.is_valid() and image_update_form.is_valid():
            user =user_update_form.save(commit=False)
            user.save()
            image_update_form.save()
            messages.success(request, "Profile updated")
            return redirect("account-profile", pk)
    else:
        user_update_form = AccountUpdateForm(instance=request.user)
        image_update_form = ProfileUpdateForm(instance=profile)
    context = {
        "user_update_form":user_update_form,
        "image_update_form":image_update_form
    }
    return render(request, template_name, context)
