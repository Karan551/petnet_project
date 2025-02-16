from django.contrib import admin
from . models import UserProfile,AuthStatus


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AuthStatus)
