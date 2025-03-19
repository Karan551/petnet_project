from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile
from django.contrib.auth.models import User
from store.models import Product
from django.contrib.auth.models import User
from .utils import user_mail
from .models import AuthStatus
from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.contrib.auth.hashers import make_password
from store.models import Product, OrderItems, Order
from django.contrib.auth.decorators import login_required
# Create your views here.


def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # print("this is form errors", form.errors)
        print("this is form.valid", form.is_valid())
        print("this is form.errors", form.errors)
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

        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfully.")
                # redirect user

                return redirect("core:home")
            else:
                messages.error(
                    request, "Invalid credentials. Please try again.")

        else:
            messages.error(request, "Something went wrong.")

    form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "userprofile/login.html", context)


def user_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logout Successfully.")
        return redirect("core:home")


def user_reset_password(request):
    error_message = None
    if request.method == "POST":

        email = request.POST.get("email", "")

        try:
            reg_user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            error_message = "User not found with this email."

        if email and reg_user:
            # 1. to store token in db  and expiry time
            # 2. to send user email and send token and expiry time

            user_mail(request, "Reset Your Password", reg_user)
            messages.success(request, "Link Send successfully.")
            return redirect("core:home")

        else:
            messages.error(request, "User not found with this email.")

    return render(request, "userprofile/password_reset.html", {'error_message': error_message})


def user_reset_password_confirm(request):
    token = request.GET.get("token", "")

    if token:

        user_status = get_object_or_404(AuthStatus, reset_token=token)

        if timezone.now() > user_status.reset_token_expiry:
            messages.error(request, "token has expired please reset again.")
            return redirect("userprofile:reset_password")

        if request.method == "POST":
            new_pwd = request.POST.get("new_password1", "")
            confirm_pwd = request.POST.get("new_password2", "")

            if new_pwd != confirm_pwd:
                messages.error(
                    request, "Confirm Password And New Password should be same.")
                return redirect("userprofile:reset_password")

            else:
                user = User.objects.get(id=user_status.user.id)

                if not user.is_superuser:
                    user.password = make_password(confirm_pwd)
                    user.save()
                    user_status.delete()

                    messages.success(request, "Password Updated Successfully.")
                    return redirect("userprofile:login")

                else:

                    # if user is admin then do this
                    user_status.delete()

                    messages.error(
                        request, "You don't have the rights to change the password.")
                    return redirect("userprofile:reset_password")

        return render(request, "userprofile/password_reset_confirm.html")

    else:
        return HttpResponseBadRequest()


def vender_detail(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        "user": user,
    }

    return render(request, "userprofile/vendor_detail.html", context)


def my_account(request):
    return render(request, "userprofile/account.html")

@login_required
def my_store(request):
    products = request.user.products.filter(status=Product.ACTIVE)
    print("this is product::", products)

    order_items = OrderItems.objects.filter(product__vendor=request.user)
    
    context = {
        "products": products,
        "order_items": order_items
    }
    return render(request, "userprofile/my_store.html", context)

@login_required
def my_store_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    is_vendor = False
    total_price = 0
    
    for item in order.orders.all():
        total_price += item.price

        if item.product.vendor == request.user:
            is_vendor = True
            
    context = {
        "order": order,
        "total_price": total_price,
        "is_vendor": is_vendor

    }

    return render(request, "userprofile/my_store_order_detail.html", context)
