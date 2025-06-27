import os
import requests
import json

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

model = "gemini-1.5-pro-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GEMINI_API_KEY}"

headers = {
    "Content-Type": "application/json"
}

prompt = (
    "Generate a list of 5 YouTube video topics related to how developers can use AI tools like Gemini, "
    "GitHub Copilot, or LLMs. Make the topics short, professional, and interesting."
)

body = {
    "contents": [{
        "parts": [{
            "text": prompt
        }]
    }]
}

response = requests.post(API_URL, headers=headers, data=json.dumps(body))

if response.status_code == 200:
    result = response.json()
    text = result['candidates'][0]['content']['parts'][0]['text']
    topics = [line.strip('- ').strip() for line in text.strip().split('\n') if line.strip()]
    with open("topics.txt", "w") as f:
        f.write('\n'.join(topics))
    print("✅ Generated topics.txt with Gemini.")
else:
    print("❌ Gemini API error:", response.status_code, response.text)
    exit(1)
