import os
import json
import requests
from config import Config

def yandex_gpt_query(system_prompt, user_query):
    """
    Отправляет запрос в Yandex GPT и возвращает ответ.
    """
    API_KEY = Config.YANDEX_API_KEY
    FOLDER_ID = Config.YANDEX_FOLDER_ID
    model_uri = f"gpt://{FOLDER_ID}/yandexgpt/latest"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "x-folder-id": FOLDER_ID,
    }

    print(API_KEY)

    data = {
        "modelUri": model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 2000,
        },
        "messages": [
            {
                "role": "system",
                "text": system_prompt,
            },
            {
                "role": "user",
                "text": user_query,
            },
        ],
    }

    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers,
        data=json.dumps(data),
    )

    if response.status_code == 200:
        return {
            "status": "success",
            "answer": response.json().get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', ''),
            "error": ""
        }
    return {
        "status": "failure",
        "answer": "",
        "error": f'Ошибка от Yandex GPT API: {response.text}'
    }

def natural_language_to_sql(user_query, schema_data):
    """
    Преобразует запрос пользователя из естественного языка в SQL-запрос с помощью LLM.
    """
    system_prompt, query = generate_prompt(user_query, schema_data)
    response = yandex_gpt_query(system_prompt, query)
    if response['status'] == 'success':
        try:
            answer = json.loads(response['answer'])
        except json.JSONDecodeError:
            answer = {
                'sql': '',
                'error_description': 'Ошибка при разборе ответа от LLM.'
            }
            print(response)
    else:
        answer = {
            'sql': '',
            'error_description': f"Ошибка от LLM: {response['error']}"
        }
    print(answer)
    return answer

def generate_prompt(user_query, schema_data):
    """
    Генерирует промпт для LLM, включая схему базы данных и запрос пользователя.
    """
    with open('prompts/sql_generation_prompt.txt', 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.replace('{schema_data}', schema_data)
    return prompt, user_query

