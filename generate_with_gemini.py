import os
import sys
import time
import google.generativeai as genai

# Load API key
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

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def retry_generate(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text:
                return text
        except Exception as e:
            print(f"⚠️ Gemini error (attempt {attempt + 1}): {e}")
            time.sleep(2)
    return ""

# 1. Generate script
script_prompt = (
    f"Write a short YouTube video script from a developer's perspective on the topic: {topic}. "
    "The script should be concise, under 60 seconds, informative, practical, and avoid marketing fluff. "
    "Use clear language. Format it naturally as if spoken by a developer. Avoid including stage directions like '(Intro)' or '(Scene)'."
)
script = retry_generate(script_prompt)

if not script:
    print("❌ Failed to generate script.")
    exit(1)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

# 2. Generate metadata: title, description, tags
title_prompt = f"Generate an engaging YouTube video title (under 60 characters) for: {topic}"
title = retry_generate(title_prompt)

description_prompt = f"Write a short YouTube description (1-2 lines) for a video about: {topic}, targeting developers."
description = retry_generate(description_prompt)

tags_prompt = f"Generate 5 to 7 relevant YouTube hashtags for: {topic}. Return them comma-separated, no numbering, just tags like: #AI, #Coding, #DevTips"
tags = retry_generate(tags_prompt)

# Write metadata to files (with safe defaults)
with open("title.txt", "w", encoding="utf-8") as f:
    f.write(title if title else topic)

with open("description.txt", "w", encoding="utf-8") as f:
    f.write(description if description else f"A quick look at {topic} from a developer’s view.")

with open("tags.txt", "w", encoding="utf-8") as f:
    f.write(tags if tags else "#AI, #Coding, #Gemini, #Shorts, #Developers")

print(f"✅ script.txt, title.txt, description.txt, tags.txt generated for topic: {topic}")
