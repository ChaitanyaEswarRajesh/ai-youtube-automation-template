import os
import requests
import base64
import time

DID_API_KEY = os.getenv("DID_API_KEY")
if not DID_API_KEY:
    print("❌ Missing D-ID API key.")
    exit(1)
os.makedirs("output", exist_ok=True)
image_path = "lady_avatar.jpg"
audio_path = "output/audio_0.wav"

# Upload image
with open(image_path, "rb") as img_file:
    img_data = img_file.read()
    img_b64 = base64.b64encode(img_data).decode()

image_upload = requests.post(
    "https://api.d-id.com/images",
    headers={
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "image": img_b64
    }
)

if image_upload.status_code != 200:
    print("❌ Failed to upload image:", image_upload.text)
    exit(1)

image_url = image_upload.json().get("url")

# Encode audio
with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

# Request talking video
video_request = requests.post(
    "https://api.d-id.com/talks",
    headers={
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "script": {
            "type": "audio",
            "audio_url": f"data:audio/wav;base64,{audio_b64}"
        },
        "source_url": image_url
    }
)

if video_request.status_code != 201:
    print("❌ Failed to generate video:", video_request.text)
    exit(1)

video_url = video_request.json().get("result_url")

# Wait and download the video
for _ in range(10):
    video_response = requests.get(video_url)
    if video_response.status_code == 200:
        with open("output/talking_avatar.mp4", "wb") as f:
            f.write(video_response.content)
        print("✅ Avatar video saved to output/talking_avatar.mp4")
        break
    time.sleep(3)
else:
    print("⚠️ Video generation not completed in time.")
