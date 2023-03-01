import os
import json
import requests
import openai
from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY

cookies = {
    '_ga': 'GA1.1.2069351461.1675500759',
    '__cf_bm': 'tKBE1CoA6B1qnHf2RHd.ue8Gx9YhVDb.XMdrxntXKSw-1677330461-0-AXvkswhQmMCVUfe8A1InxmDdQS72RXfQxJjE2pEZ17ZPdoFd1Uhiszi3g4IZwYKs+Y5Rx6q5sQr0bmTv7aMmmQgBDmgu3xpD2YIyGM9fVEBskFAz+cs2DFrNGi6iERk4rivkFNyIrXeCumeeieDciFc=',
    '_ga_XCLTX4ZEX8': 'GS1.1.1677328350.1.1.1677330711.26.0.0',
    'mp_6d31cd4238973a84421371ef3929c915_mixpanel': '%7B%22distinct_id%22%3A%20%221861ba0a4d036c-0970fa526e5568-976273f-1fa400-1861ba0a4d117f%22%2C%22%24device_id%22%3A%20%221861ba0a4d036c-0970fa526e5568-976273f-1fa400-1861ba0a4d117f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24search_engine%22%3A%20%22google%22%7D',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://phind.com',
    'Content-Type': 'application/json',
    'Origin': 'https://phind.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

def search_GPT(search_query):

    init_json_data = {
        'freshness': '',
        'q': search_query,
        'userRankList': {
            'developer.mozilla.org': 1,
            'github.com': 1,
            'stackoverflow.com': 1,
            'www.reddit.com': 1,
            'en.wikipedia.org': 1,
            'www.amazon.com': -1,
            'www.quora.com': -2,
            'www.pinterest.com': -3,
            'rust-lang': 2,
            '.rs': 1,
        },
    }

    support_response = requests.post(settings.INTERNET_SEARCH_URL, 
                                    cookies=cookies, 
                                    headers=headers, 
                                    json=init_json_data)

    json_data = {
        'question': search_query,
        'bingResults': {
            '_type': 'SearchResponse',
            'queryContext': {
                'originalQuery': search_query,
            },
            'webPages': {},
            'rankingResponse': {},
        },
    }

    raw_data = json.loads(support_response.text)
    json_data['bingResults']['webPages'] = raw_data['processedBingResults']['webPages']
    json_data['bingResults']['rankingResponse'] = raw_data['processedBingResults']['rankingResponse']

    response = requests.post(settings.INTERNET_SCRAPE_URL, 
                            cookies=cookies, 
                            headers=headers, 
                            json=json_data)
    text = response.text

    prompt = text.split('{"sentence":')
    message = [(i.split(', "sentence_source_text":')[0]).replace('"','') for index,i in enumerate(prompt) if index%2==1]
    message = ' '.join(message)
    final_message = generate_response(f"Explain this message in a much better and comprehensive manner: {message} with considering the following context: {search_query}.")
    url = [(((i.split('"url": ')[1]).split('}'))[0].replace('"','')) for index,i in enumerate(prompt) if index%2==1 and (((i.split('"url": ')[1]).split('}'))[0].replace('"',''))!='']
    url = list(set(url))
    url = '\n'.join(url)

    return final_message, url

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
        return str(response['data'][0]['url'])
    except Exception as e:
        if "request was rejected" in str(e):
            return 'Please do not violate the terms and conditions or else the account will be suspended.'
        else:
            return 'Sorry, I lost connection with my server. Please try again.'