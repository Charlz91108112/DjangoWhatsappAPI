from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .models import UserProfile, Subscription

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Subscription)

