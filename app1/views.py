import os

from dotenv import load_dotenv

load_dotenv()

import random

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Your Gemini Project ID (as a string)
PROJECT_ID = "591725467438"

# Function to generate a random 10-word heading using Gemini
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


# Main view to serve the h1 content
def api_content(request):
    # Fetch content from the API
    dynamic_content = generate_random_heading()
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Beautiful Header</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}
            .container {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                height: 100vh;
                padding: 0 20px;
                background-color: #f0f0f0;
            }}
            .left {{
                text-align: center;
            }}
            .right {{
                text-align: center;
            }}
            button {{
                padding: 10px 20px;
                font-size: 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            h1 {{
                font-size: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="col-md-6 left">
                    <h1 class="display-4">{dynamic_content}</h1>
                    <button class="btn btn-primary">Click Me</button>
                </div>
                <div class="col-md-6 right">
                    <img src="https://via.placeholder.com/400" alt="Beautiful Image" class="img-fluid">
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """)
