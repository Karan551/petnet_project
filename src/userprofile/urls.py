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
    
    path("vender-detail/<int:user_id>/", views.vender_detail, name="vender_detail"),
    
    path("reset-password/",views.user_reset_password,name="reset_password"),
    
    path("reset-password-confirm/",views.user_reset_password_confirm,name="reset_password_confirm"),
    
    # path("password-reset-confirm/<uidb64>/<token>/",views.ConfirmPasswordView.as_view(),name="password_reset_confirm"),
    # path("password_reset_complete/",PasswordResetCompleteView.as_view(
    #     template_name="userprofile/password_reset_complete.html"
    #     ),name="password_reset_complete"),
    
]
