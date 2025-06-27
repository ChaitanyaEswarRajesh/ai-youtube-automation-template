
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = (
    "Generate 10 YouTube video topics for software developers interested in AI. "
    "Topics should be practical, technical, and appealing to developers."
)

response = model.generate_content(prompt)
topics = response.text.strip().split("\n")
with open("topics_master.txt", "a", encoding="utf-8") as f:
    for t in topics:
        if t.strip():
            f.write(t.strip().lstrip("-• ") + "\n")
print("✅ New topics appended to topics_master.txt")
