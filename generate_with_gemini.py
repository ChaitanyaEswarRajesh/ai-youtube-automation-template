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

# === 1. Generate script ===
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

# === 2. Generate metadata ===
title_prompt = (
    f"Generate ONE engaging YouTube video title under 60 characters for the topic: {topic}. "
    "Return only the title text, no bullet points, no quotes."
)
title = retry_generate(title_prompt).split("\n")[0].strip()
if len(title) > 60:
    title = title[:60].strip()

description_prompt = f"Write a short YouTube description (1-2 lines) for a video about: {topic}, targeting developers."
description = retry_generate(description_prompt).strip()

tags_prompt = (
    f"Generate 5 to 7 relevant YouTube hashtags for: {topic}. "
    "Return them comma-separated, no numbering, just tags like: #AI, #Coding, #DevTips"
)
tags_raw = retry_generate(tags_prompt)

# Normalize tags
hashtags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()] if tags_raw else []
if "#shorts" not in [tag.lower() for tag in hashtags]:
    hashtags.append("#shorts")
if not hashtags:
    hashtags = ["#AI", "#Coding", "#Gemini", "#Shorts", "#Developers"]

# Fallbacks
final_title = title if title else topic
final_description = description if description else f"A quick look at {topic} from a developer’s view."
if "#shorts" not in final_description.lower():
    final_description += " #shorts"

# === Save to files ===
with open("title.txt", "w", encoding="utf-8") as f:
    f.write(final_title)

with open("description.txt", "w", encoding="utf-8") as f:
    f.write(final_description)

with open("tags.txt", "w", encoding="utf-8") as f:
    f.write(", ".join(hashtags))

# === Log ===
print("✅ Metadata generated:")
print("• Title:", final_title)
print("• Description:", final_description)
print("• Tags:", ", ".join(hashtags))
print(f"✅ script.txt, title.txt, description.txt, tags.txt saved for topic: {topic}")
