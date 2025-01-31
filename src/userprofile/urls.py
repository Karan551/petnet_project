from django.urls import path
from . import views

app_name = "userprofile"

urlpatterns = [
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("my-account/", views.my_account, name="my_account"),
    path("my-store/", views.my_store, name="my_store"),
    
    path("vender-detail/<int:user_id>", views.vender_detail, name="vender_detail"),
]
