from django.urls import path
from . import views


urlpatterns = [
path('',views.home, name='home'),
# TODO: Here replace the webhook-code with before initialization
path('webhook-code',views.WhatsappWebhook, name = 'whatsapp-webhook'),
]
