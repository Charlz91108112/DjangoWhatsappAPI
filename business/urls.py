from django.urls import path
from . import views


urlpatterns = [
path('',views.home, name='home'),
path('webhook-code',views.WhatsappWebhook, name = 'whatsapp-webhook'),
]
