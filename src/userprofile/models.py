from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="userprofile", on_delete=models.CASCADE)

    is_vendor = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User Profile"

    def __str__(self):
        return self.user.username


class AuthStatus(models.Model):
    user = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE)
    verify_token = models.CharField(max_length=300, blank=True, null=True)
    verify_token_expiry = models.DateTimeField(null=True, blank=True)
    reset_token = models.CharField(
        max_length=300, blank=True, null=True)  # Store token as string
    reset_token_expiry = models.DateTimeField(
         null=True, blank=True)  # When the token expires
    # Whether the user is authenticated (logged in or not)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def is_token_expired(self):
        return timezone.now() > self.token_expiry

    def __str__(self):
        return f"Password Reset for {self.user.email}"

    class Meta:
        verbose_name_plural = "Auth Status"
