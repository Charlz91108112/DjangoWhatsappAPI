from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
from django.urls import reverse
import json
import os

# 1) The UserProfile Module
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=False)
    phone_ID = models.CharField(max_length=40, blank=False)
    uniqueID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.now()
        # self.last_updated = timezone.now()
        return super(UserProfile, self).save(*args, **kwargs)

class Subscription(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=20, blank=True, default="Free")
    subscription_status = models.CharField(max_length=20, blank=True, default="Active")
    subscription_start_date = models.DateTimeField(auto_now_add=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True)
    history_text_prompt = models.TextField(blank=True)
    history_image_prompt = models.TextField(blank=True)
    free_prompt_count = models.IntegerField(default=0)
    free_image_count = models.IntegerField(default=0)
    uniqueID = models.UUIDField(default=uuid4, editable=False)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.subscription_start_date is None and self.subscription_type != "Free":
            self.subscription_start_date = timezone.now()
        # self.last_updated = timezone.now()
        return super(Subscription, self).save(*args, **kwargs)
