import os
import sys
import google.generativeai as genai

# Load Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ Missing GEMINI_API_KEY in environment.")
    exit(1)

# Load topic from CLI arg or fallback to topics.txt
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

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Prompt for the script
prompt = (
    f"Write a short YouTube video script from a developer's perspective on the topic: {topic}. "
    "The script should be concise, under 60 seconds, informative, practical, and avoid marketing fluff. "
    "Use simple, clear language. It should read like a developer speaking to other developers."
)

# Generate content
try:
    response = model.generate_content(prompt)
    script = response.text.strip()

    if not script:
        print("❌ Empty response from Gemini.")
        exit(1)

    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print(f"✅ Generated script.txt for topic: {topic}")
except Exception as e:
    print("❌ Gemini API error:", e)
    exit(1)
