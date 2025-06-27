import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
import google.oauth2.credentials
import requests

def upload_video(filename, title, description, tags, privacy="public", thumbnail_path=None):
    credentials = google.oauth2.credentials.Credentials(
        token=None,
        refresh_token=os.getenv("YT_REFRESH_TOKEN"),
        client_id=os.getenv("YT_CLIENT_ID"),
        client_secret=os.getenv("YT_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    credentials.refresh(google.auth.transport.requests.Request())
    youtube = build("youtube", "v3", credentials=credentials)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags.split(","),
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": privacy
        }
    }

    media = MediaFileUpload(filename, chunksize=-1, resumable=True)
    upload_request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = upload_request.next_chunk()
        if response and "id" in response:
            print(f"✅ Video uploaded: https://youtu.be/{response['id']}")
            if thumbnail_path:
                youtube.thumbnails().set(
                    videoId=response["id"],
                    media_body=MediaFileUpload(thumbnail_path)
                ).execute()
                print("🖼️ Thumbnail uploaded.")
        elif status:
            print(f"Uploading... {int(status.progress() * 100)}%")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python upload_to_youtube.py [full|short] [index]")
        exit(1)

    mode = sys.argv[1]
    index = sys.argv[2]

    title = open("title.txt").read().strip()
    description = open("description.txt").read().strip()
    tags = open("tags.txt").read().strip()

    filename = f"output/video_{mode}_{index}.mp4"
    thumbnail = f"output/image_{index}.jpg"

    upload_video(filename, title, description, tags, thumbnail_path=thumbnail)
