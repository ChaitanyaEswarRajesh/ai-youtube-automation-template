import os
import subprocess

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Read topics from topics.txt
with open("topics.txt", "r") as f:
    topics = [line.strip() for line in f if line.strip()]

# Loop through topics
for i, topic in enumerate(topics):
    print(f"\n🚀 Processing Topic {i+1}: {topic}")

    # Simulate script generation using Gemini script (or manual fallback)
    with open("script.txt", "w") as sfile:
        sfile.write(f"This is a local test video about: {topic}. No Gemini tokens were used.")

    # Text-to-Speech using Coqui TTS
    audio_path = f"output/audio_{i}.wav"
    subprocess.run([
        "tts", "--text", open("script.txt").read(),
        "--model_name", "tts_models/en/ljspeech/tacotron2-DDC",
        "--out_path", audio_path
    ], check=True)

    # Simulated image (static fallback image)
    image_path = f"output/image_{i}.jpg"
    subprocess.run([
        "wget", "-O", image_path,
        "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg"
    ], check=True)

    # Generate subtitle (.srt) file
    srt_path = f"output/subtitles_{i}.srt"
    with open(srt_path, "w") as srt:
        srt.write(f"""1
00:00:00,000 --> 00:00:10,000
{topic}
""")

    # Generate video with FFmpeg
    video_path = f"output/video_{i}.mp4"
    subprocess.run([
        "ffmpeg", "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-vf", f"subtitles={srt_path}",
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-shortest", "-y", video_path
    ], check=True)

    print(f"✅ Video saved to {video_path}")
    print(f"📝 Subtitle saved to {srt_path}")
