import os
import requests
import json

import logging
logger = logging.getLogger(__name__)


    

def get_promt(catalog, temperature, api_key, profession, work_experience, work_skills):

    modelUri = f"gpt://{catalog}/yandexgpt-lite"
    completionOptions = {
        "stream": False,
        "temperature": temperature,
        "maxTokens": "2000"
        }
    messages = [
        {
            "role": "system",
            "text": "Ты профессиональный дизанер создающий промты для генерации изображений на футбулках. В ответ ты возвращаешь только промт не добавляешь ничего от себя"
        },
        {
            "role": "user",
            "text": "Cоздай промт для генерации изображения на футболку для человека с профессией Сантехник-электрик со стажем работы 5 лет и профессиональными навыками: Электромонтажные работы, электрика, сантехнические работы. По этому промту нейросеть для генерации изображений должна сгенерировать красивую и четкую картинку для печати на майке. За хороший промт получишь чаевые 10$"
        },
        {
            "role": "assistant",
            "text": "по центру изображения человек профессии - сантехник-электрик. Покажите нарисованный электрический провод, переходящий в трубу с водой, символизируя сочетание электромонтажных и сантехнических работ. Добавьте молнию как элемент электрики и гаечный ключ как символ профессиональных навыков. Учтите, что человеку с 5-летним стажем работы это должно быть интересно и профессионально выглядеть."
        },
        {
            "role": "user",
            "text": f"Создай промт для генерации изображения на футболку для человека с профессией {profession} со стажем работы {work_experience} лет и профессиональными навыками: {work_skills}По этому промту нейросеть для генерации изображений должна сгенерировать красивую и четкую картинку для печати на майке. За хороший промт получишь чаевые 10$"
        }
    ]

    prompt = {
        "modelUri": modelUri,
        "completionOptions": completionOptions,
        "messages": messages
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization":  f"Api-Key {api_key}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response
    return result



catalog = os.environ.get('CATALOG')
api_key = os.environ.get('API_KEY')



def get_image(catalog, api_key, text_promt):

    modelUri = f"art://{catalog}/yandex-art/latest"

    generationOptions = {
    "mimeType": "image/jpeg",
    "seed": 42
    }

    body_image = {
        "modelUri": modelUri,
        "messages":[{"text": text_promt, "weight": 1}],
        "generationOptions": generationOptions
    }  
    

    url = " https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
        "Content-Type": "application/json",
        "Authorization":  f"Api-Key {api_key}"
    }


    response = requests.post(url, headers=headers, json=body_image)
    result = response
    return result



def handler(event, context):
    body = json.loads(event['body'])

    
    profession = body['profession']
    work_experience = body['work_experience']
    work_skills = body['work_skills']

    promt_gpt = get_promt(catalog, 0.6, api_key, profession, work_experience, work_skills)
    text_promt = promt_gpt.json()['result']['alternatives'][0]['message']['text']

    # text_promt = 'котик красно бело синий'
    if len(text_promt)> 500:
        text_promt = text_promt[:500]
    
    image_info = get_image(catalog, api_key, text_promt)
    
    
    return {
        'statusCode': 200,
        'body': {'image': image_info.json()['id']},
    }
