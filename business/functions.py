from django.conf import settings
import requests
from .models import UserProfile, Subscription
from django.contrib.auth.models import User
from .openai_API import generate_response, generate_image, search_GPT
import asyncio

loop = asyncio.new_event_loop()


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

def sendWhatsAppImage(phoneNumber, link):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": "image",
        "image": {"link": link}
    }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    return response.json()

def process_text_async(text, subscribe, fromID):
    message = generate_response(text.split('#')[1])
    if message:
        subscribe.free_prompt_count += 1
        subscribe.history_text_prompt += f"{text}.\n"
        subscribe.save()
    sendWhatsAppMessage(fromID, message)

def process_image_async(text, subscribe, fromID):
    message = generate_image(text.split('##')[1])
    if "https" in message:
        subscribe.free_image_count += 1
        subscribe.history_image_prompt += f"{text}.\n"
        subscribe.save()
        sendWhatsAppImage(fromID, message)
    else:
        sendWhatsAppMessage(fromID, message)

def process_text_internet_async(text, subscribe, fromID):
    message, urls = search_GPT(text.split('@')[1])
    if message:
        subscribe.free_prompt_count += 1
        subscribe.history_text_prompt += f"{text}.\n"
        subscribe.save()
    sendWhatsAppMessage(fromID, f"{message}\n\n{urls}")
    


def handleWhatsappReply(phoneID, profileName, fromID, text):
    # Check if the user already exist?
    try:
        #sendWhatsAppMessage(fromID, "Checking if the user already exist!")
        subscribe = Subscription.objects.get(profile__phone_number=fromID)
        if subscribe.free_prompt_count > 50:
            message = "Sorry, you can only send 50 free prompts in your free quota.\n\nKind Regards.\nWhatsAppGPT"
            sendWhatsAppMessage(fromID, message)
            return
        elif subscribe.free_image_count > 20:
            message = "Sorry, you can only send 20 free images in your free quota.\n\nKind Regards.\nWhatsAppGPT"
            sendWhatsAppMessage(fromID, message)
            return
        else:
            if text.startswith('#') and text.count('#') == 1:
                loop.run_in_executor(None, process_text_async, text, subscribe, fromID)
            elif text.startswith('##') and text.count('##') == 1:
                loop.run_in_executor(None, process_image_async, text, subscribe, fromID)
            elif text.startswith('@') and text.count('@') == 1:
                loop.run_in_executor(None, process_text_internet_async, text, subscribe, fromID)
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
                subscribe = Subscription.objects.create(profile=user_profile,
                                                        profileName=profileName,)
                message = (f'Hello {profileName}!\n\n' + 
                            'I am WhatsApp GPT which help you write better and faster.' + 
                            'Just ask me to frame or write anything for you I will try my best.\n\n' + 
                            'In order to get started use this format to ask me anythin:\n\n' + 
                            '#Write me an email for the leave that I can send to HR\n\n' + 
                            'Kind Regards\nWhatsappGPT')

                sendWhatsAppMessage(fromID, message)
            #subscribe = Subscription.objects.create(profile=user_profile)
        except Exception as e:
            sendWhatsAppMessage(fromID, str(e))
