import os
import requests
import json


    

def get_image_jpg(api_key, request_id):


    url = f"https://llm.api.cloud.yandex.net/operations/{request_id}"

    headers = {
        "Authorization":  f"Api-Key {api_key}"
    }

    response = requests.get(url, headers=headers)
    result = response
    return result


api_key = os.environ.get('API_KEY')


def handler(event, context):
    body = json.loads(event['body'])
    # body = event['body']

    
    image_id = body['image_id']
    return_data = get_image_jpg(api_key, image_id)
    
    return {
        'statusCode': 200,
        'body': {'data': return_data.json()},
    }
