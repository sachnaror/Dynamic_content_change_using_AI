import os

import requests
from django.http import JsonResponse
from django.shortcuts import render


def generate_random_heading():
    api_key = os.getenv("API_KEY")
    if not api_key:
        return "Error: API key is not set."

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateText?key={api_key}'

    headers = {'Content-Type': 'application/json'}
    payload = {
        'model': 'gemini-1.5-flash',  # Ensure this matches the correct model name
        'prompt': {
            'text': 'Generate a 10-word heading.'  # This might need to be adjusted based on documentation
        },
        'temperature': 0.7,
        'maxOutputTokens': 15  # Correct field name as per updated documentation
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data['candidates'][0]['content']  # Adjust if the structure is different
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err} - {response.text}"  # Log full response text for debugging
    except Exception as err:
        return f"Other error occurred: {err}"

def index(request):
    dynamic_content = generate_random_heading()  # Generate the dynamic content
    return render(request, 'app1/index.html', {'dynamic_content': dynamic_content})

