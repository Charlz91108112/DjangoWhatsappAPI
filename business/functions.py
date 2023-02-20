from django.conf import settings
import requests
from .models import UserProfile, Subscription
from django.contrib.auth.models import User
from .openai_API import generate_response


def sendWhatsAppMessage(phoneNumber, message):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    return response.json()

def handleWhatsappReply(phoneID, profileName, fromID, text):
    # Check if the user already exist?
    try:
        #sendWhatsAppMessage(fromID, "Checking if the user already exixt!")
        subscribe = Subscription.objects.get(profile__phone_number=fromID)
        if subscribe.free_prompt_count > 10:
            message = "Sorry, you can only send 10 free prompts in your free quota.\n\nKind Regards.\nWhatsAppGPT"
            sendWhatsAppMessage(fromID, message)
            return
        else:
            if text.startswith('#'):
                message = generate_response(text.split('#')[1])
                #message = "Some problem with OPENAI"
                if message:
                    subscribe.free_prompt_count += 1
                    subscribe.save()
            else:
                message = "Sorry the format of the question is not proper and I am not able to answer it.\n\nKind Regards.\nWhatsAppGPT"
            sendWhatsAppMessage(fromID, message)

    except Exception as e:
        #sendWhatsAppMessage(fromID, f"Issue with top function -- {e}")
        try:
            if User.objects.filter(username=fromID).exists():
                user = User.objects.get(username=fromID)
                user_profile = UserProfile.objects.get(user=user)
            else:
                user = User.objects.create_user(username=fromID, 
                                                password=phoneID, 
                                                )
                user_profile = UserProfile.objects.create(user=user,
                                                    phone_number=fromID,
                                                    phone_ID=phoneID,)
                subscribe = Subscription.objects.create(profile=user_profile)
                message = (f'Hello {profileName}!\n\n.' + 
                            'I am WhatsApp GPT which help you write better and faster.' + 
                            'Just ask me to frame or write anything for you I will try my best.\n\n' + 
                            'In order to get started use this format to ask me anythin:\n\n' + 
                            '#Write me an email for the leave that I can send to HR\n\n' + 
                            'Kind Regards\nWhatsappGPT')

                sendWhatsAppMessage(fromID, message)
            #subscribe = Subscription.objects.create(profile=user_profile)
        except Exception as e:
            sendWhatsAppMessage(fromID, str(e))