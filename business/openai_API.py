import os
import openai
from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY

def generate_response(prompt):
    try:
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Understand the following prompt thoroughly: {prompt}. Now act as an expert and provide the comprehensive answer to it in less than 150 words. Make sure to add wit to make it look like humanly as possible. Make everything sound perfect. If someone has asked for a coding problem then make sure to provide the complete code.",
        temperature=0.9,
        max_tokens=3200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        return response['choices'][0]['text']
    except Exception as e:
        return 'Sorry, I lost connection with my server. Please try again.'

def generate_image(prompt):
    try:
        response = openai.Image.create(
        prompt=f"{prompt}",
        n=1,
        size="1024x1024"
        )
        return response['data'][0]['url']
    except Exception as e:
        if "request was rejected" in str(e):
            return 'Please do not violate the terms and conditions or else the account will be suspended.'
        else:
            return 'Sorry, I lost connection with my server. Please try again.'