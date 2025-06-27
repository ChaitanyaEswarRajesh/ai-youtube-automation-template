import os
import sys
import time
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ Missing GEMINI_API_KEY in environment.")
    exit(1)

# Get topic from CLI or fallback to topics.txt
if len(sys.argv) >= 2:
    topic = sys.argv[1]
else:
    if not os.path.exists("topics.txt") or os.path.getsize("topics.txt") == 0:
        print("❌ No topic provided and topics.txt is empty or missing.")
        exit(1)
    with open("topics.txt", "r") as f:
        topic = f.readline().strip()

if not topic:
    print("❌ Topic is empty.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def retry_generate(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ Gemini error (attempt {attempt+1}): {e}")
            time.sleep(2)
    return ""

# Main script
script_prompt = (
    f"Write a short YouTube video script from a developer's perspective on the topic: {topic}. "
    "The script should be concise, under 60 seconds, informative, practical, and avoid marketing fluff. "
    "Use simple, clear language. It should read like a developer speaking to other developers."
)
script = retry_generate(script_prompt)

if not script:
    print("❌ Failed to generate script.")
    exit(1)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

# Generate metadata
title = retry_generate(f"Generate a YouTube title for this topic: {topic}. Keep it under 60 characters.")
description = retry_generate(f"Write a short YouTube video description (1-2 lines) about: {topic}.")
tags = retry_generate(f"Suggest 5 relevant YouTube hashtags (comma-separated) for the topic: {topic}.")

with open("title.txt", "w", encoding="utf-8") as f:
    f.write(title or topic)

with open("description.txt", "w", encoding="utf-8") as f:
    f.write(description or f"A quick video about {topic} for developers.")

with open("tags.txt", "w", encoding="utf-8") as f:
    f.write(tags or "#AI, #Coding, #DevTips, #Gemini, #Tech")

print(f"✅ script.txt, title.txt, description.txt, tags.txt generated for topic: {topic}")
