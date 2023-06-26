import contextlib
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .functions import *
import json


# Create your views here.
def home(request):
    return render(request, 'business/index.html',{})

@csrf_exempt
def WhatsappWebhook(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode and token:
            VERIFY_TOKEN = ''
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return HttpResponse(challenge, status = 200)
            else:
                return HttpResponse('error' , status = 403)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (
            'object' in data
            and 'entry' in data
            and data['object'] == 'whatsapp_business_account'
        ):
            try:
                for entry in data['entry']:
                    phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                    phoneID = entry['changes'][0]['value']['metadata']['phone_number_id']
                    profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                    whatsappID = entry['changes'][0]['value']['contacts'][0]['wa_id']
                    fromID = entry['changes'][0]['value']['messages'][0]['from']
                    messageID = entry['changes'][0]['value']['messages'][0]['id']
                    timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                    text = entry['changes'][0]['value']['messages'][0]['text']['body']

                    #message = f"RE: '{text}' was received!\n\nWill get back to you shortly! Thank you for your patience!\n\n Kind Regards.\nWhatsAppGPT"
                    #sendWhatsAppMessage(fromID, "Initiaitng the send")
                    handleWhatsappReply(phoneID, profileName, fromID, text)
            except Exception as e:
                message = f"Got some error please check: {e}"
                # sendWhatsAppMessage(my_number, message)
        return HttpResponse("success", status = 200)
