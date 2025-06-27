
import os
import sys
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ Missing GEMINI_API_KEY in environment.")
    exit(1)

if len(sys.argv) < 2:
    print("❌ Missing topic. Usage: python generate_with_gemini.py 'Your Topic'")
    exit(1)

topic = sys.argv[1]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
prompt = (
    f"Write a short YouTube video script from a developer's perspective on the topic: {topic}. "
    "The script should be concise, informative, and engaging for fellow developers. Avoid marketing language."
)

try:
    response = model.generate_content(prompt)
    script = response.text
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    print("✅ Generated script.txt for topic:", topic)
except Exception as e:
    print("❌ Gemini API error:", e)
    exit(1)
