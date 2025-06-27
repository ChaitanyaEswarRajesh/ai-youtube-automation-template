import os
import google.generativeai as genai

# Load the API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Define your prompt
prompt = (
    "Generate a list of 5 YouTube video topics related to how developers can use AI tools like Gemini, "
    "GitHub Copilot, or LLMs. Make the topics short, professional, and interesting."
)

# Generate content
try:
    response = model.generate_content(prompt)
    text = response.text
    topics = [line.strip('-• ').strip() for line in text.split('\n') if line.strip()]

    # Write topics to file
    with open("topics.txt", "w") as f:
        f.write("\n".join(topics))

    print("✅ Successfully generated topics.txt using Gemini 1.5 Flash")
except Exception as e:
    print("❌ Gemini SDK error:", e)
    exit(1)
