from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="userprofile", on_delete=models.CASCADE)

    is_vendor = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User Profile"

    def __str__(self):
        return self.user.username
