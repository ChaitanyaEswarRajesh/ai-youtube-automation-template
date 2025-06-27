import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(file_path, title, description, tags, is_short=False):
    creds = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"]
    )

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags.split(","),
            "categoryId": "28"  # Tech
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = request.execute()
    print("✅ Uploaded:", response["id"])

if __name__ == "__main__":
    mode = sys.argv[1]  # full or short
    i = sys.argv[2]     # index
    title = open("title.txt").read().strip()
    description = open("description.txt").read().strip()
    tags = open("tags.txt").read().strip()

    if mode == "short":
        title += " #shorts"
        description += "\n#shorts"
        tags += ",shorts"
        file_path = f"output/video_short_{i}.mp4"
    else:
        file_path = f"output/video_full_{i}.mp4"

    upload_video(file_path, title, description, tags, is_short=(mode == "short"))
