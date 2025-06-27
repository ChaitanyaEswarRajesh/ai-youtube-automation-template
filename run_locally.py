
import os
from read_next_topic import read_next_topic

topic = read_next_topic()
if topic:
    os.system(f"python generate_with_gemini.py \"{topic}\"")
    print("🎬 Simulated local run completed.")
