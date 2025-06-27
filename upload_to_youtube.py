import os
import sys
import json
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Required secrets from environment
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
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return build("youtube", "v3", credentials=creds)

def upload_video(filename, title, description, tags, thumbnail_path=None):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [tag.strip() for tag in tags.split(",")],
            "categoryId": "28",  # Science & Technology
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(filename, mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = request.execute()
    video_id = response["id"]
    print(f"✅ Video uploaded: https://youtu.be/{video_id}")

    # Optional thumbnail (ignored for Shorts)
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            print("🖼️ Thumbnail uploaded.")
        except Exception as e:
            print("⚠️ Could not upload thumbnail:", e)

# === ENTRY POINT ===
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Usage: python upload_to_youtube.py [full|short] [index]")
        exit(1)

    mode = sys.argv[1]  # "full" or "short"
    index = sys.argv[2]

    video_file = f"output/video_{mode}_{index}.mp4"
    title = open("title.txt").read().strip()
    description = open("description.txt").read().strip()
    tags = open("tags.txt").read().strip()

    if mode == "short":
        if "#shorts" not in title.lower():
            title += " #shorts"
        if "#shorts" not in description.lower():
            description += "\n#shorts"
        if "shorts" not in tags.lower():
            tags += ",#shorts"

    upload_video(video_file, title, description, tags)
