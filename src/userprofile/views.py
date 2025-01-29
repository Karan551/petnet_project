from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile
from django.contrib.auth.models import User

# Create your views here.


def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # print("this is form errors", form.errors)

        if form.is_valid():
            user = form.save()
            print("this is user::", user)

            userprofile = UserProfile.objects.create(user=user)

            messages.success(request, "User Created Succesfully. Please Login")

            # here we redirect to login page.
            return redirect("userprofile:login")

    form = SignUpForm()
    context = {
        "form": form
    }
    return render(request, "userprofile/signup.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # print("this is username::",username,password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # print("this is user::",user)
            messages.success(request, "Login Successfully.")
            # redirect user
            # TODO: change hardcoded value
            return redirect("/")

    form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "userprofile/login.html", context)


def user_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logout Successfully.")
        # TODO: change into relative name
        return redirect("/")


def vender_detail(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        "user": user,
    }

    return render(request, "userprofile/vendor_detail.html", context)

def my_account(request):
    return render(request,"userprofile/account.html")