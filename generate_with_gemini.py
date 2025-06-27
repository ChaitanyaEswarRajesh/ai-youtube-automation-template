import os
import requests
import json
import sys

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
topic = sys.argv[1]

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

headers = {
    "Content-Type": "application/json"
}

body = {
    "contents": [{
        "parts": [{
            "text": f"Write a short YouTube video script from a developer's perspective on the topic: {topic}. Make it concise, informative, and professional."
        }]
    }]
}

response = requests.post(API_URL, headers=headers, data=json.dumps(body))

if response.status_code == 200:
    result = response.json()
    script = result['candidates'][0]['content']['parts'][0]['text']
    with open("script.txt", "w") as f:
        f.write(script)
    print("✅ Gemini script generated.")
else:
    print("❌ Gemini API error:", response.status_code, response.text)
    exit(1)
