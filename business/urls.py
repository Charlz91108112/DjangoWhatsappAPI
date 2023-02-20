from django.urls import path
from . import views


urlpatterns = [
path('',views.home, name='home'),
path('f2bfdb2c-654c-49e8-a335-14d71798a793',views.WhatsappWebhook, name = 'whatsapp-webhook'),
]
