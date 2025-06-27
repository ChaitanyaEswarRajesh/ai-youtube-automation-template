import os
import sys
import json
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
    print("❌ Missing one or more YouTube credentials.")
    exit(1)

def get_authenticated_service():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES,
    )
    creds.refresh(google.auth.transport.requests.Request())
    return build("youtube", "v3", credentials=creds)

def upload_video(filename, title, description, tags, thumbnail_path=None):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "categoryId": "28",  # Science & Technology
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(filename, mimetype="video/mp4", resumable=True)

    print(f"📤 Uploading video: {filename}")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = request.execute()
    video_id = response["id"]
    print(f"✅ Video uploaded: https://youtu.be/{video_id}")

    # Optional: upload thumbnail for full video only
    if thumbnail_path and os.path.exists(thumbnail_path) and "short" not in filename:
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            print("🖼️ Thumbnail uploaded.")
        except Exception as e:
            print("⚠️ Could not upload thumbnail:", e)

# === Entry Point ===
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("❌ Usage: python upload_to_youtube.py [full|short] [index] [title] [description] [tags]")
        exit(1)

    mode = sys.argv[1]
    index = sys.argv[2]
    title = sys.argv[3]
    description = sys.argv[4]
    tags = sys.argv[5] if len(sys.argv) >= 6 else ""

    video_file = f"output/video_{mode}_{index}.mp4"
    upload_video(video_file, title, description, tags)
