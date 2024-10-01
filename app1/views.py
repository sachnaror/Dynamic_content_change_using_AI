import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables

import random

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Your Gemini Project ID (as a string)
PROJECT_ID = "591725467438"




def generate_random_heading():
    api_key = os.getenv("API_KEY")
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    data = {"contents":[{"parts":[{"text":"Generate a random 10-word heading for a website"}]}]}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(response.json())  # Print the JSON response for inspection

        try:
            generated_text = response.json()['contents'][0]['parts'][0]['text']
            return generated_text
        except KeyError:
            return "Failed to extract text from response."
    else:
        return f"API request failed with status code {response.status_code}"


# Dedicated API view for content generation
def api_content(request):
    dynamic_content = generate_random_heading()
    return JsonResponse({'content': dynamic_content})

# Main index view
def index(request):
    # Fetch content from the API
    response = requests.get("http://127.0.0.1:8000/app1/api_content/")
    if response.status_code == 200:
        dynamic_content = response.json().get("content", "Failed to fetch content.")
    else:
        dynamic_content = "Failed to fetch content."
    return render(request, 'app1/index.html', {'dynamic_content': dynamic_content})
