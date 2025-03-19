from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetCompleteView

app_name = "userprofile"

urlpatterns = [
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("my-account/", views.my_account, name="my_account"),
    path("my-store/", views.my_store, name="my_store"),
    path("my-store-order-detail/<int:order_id>",
         views.my_store_order_detail, name="my_store_order_detail"),

    path("vender-detail/<int:user_id>/",
         views.vender_detail, name="vender_detail"),

    path("reset-password/", views.user_reset_password, name="reset_password"),

    path("reset-password-confirm/", views.user_reset_password_confirm,
         name="reset_password_confirm"),



]
