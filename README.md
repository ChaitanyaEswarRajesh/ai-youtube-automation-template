# AI YouTube Automation (Multi-Topic, Gemini + Subtitles)

This GitHub Actions workflow automates creating and uploading AI-narrated videos to YouTube using:

- ✅ Coqui TTS for voiceover
- ✅ Pixabay API for free image assets
- ✅ FFmpeg for video generation
- ✅ YouTube Data API for upload
- ✅ Gemini API (for smarter script generation)
- ✅ SRT subtitles auto-generated from narration
- ✅ Weekly scheduled uploads from a list of developer-focused AI topics

---

## ✅ Setup Instructions

### 1. GitHub Secrets Required

| Secret Name             | Purpose                                 |
|--------------------------|-----------------------------------------|
| `PIXABAY_API_KEY`       | Pixabay free image API key              |
| `YT_CLIENT_ID`          | YouTube OAuth2 Client ID                |
| `YT_CLIENT_SECRET`      | YouTube OAuth2 Client Secret            |
| `YT_REFRESH_TOKEN`      | YouTube API OAuth2 Refresh Token        |
| `GEMINI_API_KEY`        | Gemini API Key (from Google AI Studio)  |

---

## 🗓️ Automated Weekly Upload

- Topics listed in `topics.txt` are processed **once per week**.
- Each topic is:
  - Used to generate a script using Gemini
  - Converted to speech using Coqui TTS
  - Paired with a related Pixabay image
  - Combined into a video with auto-subtitles
  - Uploaded to your YouTube channel automatically

---

## 📝 topics.txt

Place all your topics (one per line) in `topics.txt`. Examples:
```
How AI like Gemini assists developers in coding
Using AI to debug software faster
AI tools for improving developer productivity
```
