import os

import requests
from django.http import JsonResponse
from django.shortcuts import render


# Function to generate a random heading using Gemini
def generate_random_heading():
    api_key = os.getenv("API_KEY")  # Ensure the API key is stored as an environment variable
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

    headers = {'Content-Type': 'application/json'}
    payload = {
        'prompt': {'text': 'Generate a 10-word heading.'},
        'temperature': 0.7,
        'maxTokens': 15
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']
    else:
        return "Error generating heading."

# View to display the dynamic heading on the webpage
def index(request):
    dynamic_content = generate_random_heading()  # Generate the dynamic content
    return render(request, 'app1/index.html', {'dynamic_content': dynamic_content})
