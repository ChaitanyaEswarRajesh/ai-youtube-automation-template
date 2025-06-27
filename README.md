# 🤖 AI YouTube Automation for Developers

This project automates the creation and upload of daily AI-generated YouTube videos from developer-focused topics using free tools and APIs like Google Gemini, D-ID, and YouTube Data API.

---

## 📦 Features

- 🔁 Automatically rotates through a list of video topics
- ✍️ Uses **Gemini** (Google AI) to generate developer-style scripts
- 🔊 Converts script to audio with **TTS** (coqui-ai TTS)
- 👩‍💻 Creates talking AI lady avatar video using **D-ID API**
- 🖼️ Falls back to static image video if avatar fails
- 🎬 Uploads both **full** and **YouTube Shorts**
- 🗓️ Fully automated via **GitHub Actions**

---

## 🧠 Workflow Overview

1. **Topic Selection**: Picks next topic from `topics_master.txt`
2. **Script Generation**: Uses `generate_with_gemini.py` to produce script, title, description, tags
3. **Audio Generation**: Text-to-speech via `tts` CLI
4. **Talking Avatar**: Uses `generate_talking_avatar.py` + D-ID API
5. **Fallback**: If avatar fails, `ffmpeg` builds a basic video
6. **Upload**: `upload_to_youtube.py` handles full + short uploads
7. **Runs daily via GitHub Actions**

---

## 🛠 Files & Structure

```bash
.
├── .github/workflows/daily_video.yml        # GitHub Actions automation
├── auto_generate_topics.py                  # (Optional) Generate topic list using LLM
├── generate_with_gemini.py                  # Uses Gemini to create script + metadata
├── generate_talking_avatar.py               # D-ID avatar video generator
├── upload_to_youtube.py                     # Uploads MP4s using YouTube Data API
├── lady_avatar.jpg                          # Avatar image used for AI video
├── topics_master.txt                        # Master list of all topics to process
├── topics.txt                               # Holds current topic being processed
├── requirements.txt                         # All Python dependencies


⚙️ Setup & Secrets
Required GitHub Secrets
| Name               | Purpose                               |
| ------------------ | ------------------------------------- |
| `GEMINI_API_KEY`   | Gemini 1.5 API Key (Google AI)        |
| `PIXABAY_API_KEY`  | Pixabay API for fetching images       |
| `DID_API_KEY`      | D-ID API Key for talking avatar       |
| `YT_CLIENT_ID`     | YouTube Data API OAuth2 client ID     |
| `YT_CLIENT_SECRET` | YouTube Data API OAuth2 client secret |
| `YT_REFRESH_TOKEN` | YouTube refresh token for upload      |


✅ Usage
Edit your topics_master.txt with new topics (1 per line)

Push code to GitHub (with secrets set)

GitHub Actions will run daily and upload videos automatically

🧹 Notes
If D-ID API fails, it will fallback to a static ffmpeg-generated video.

Only lady_avatar.jpg is used for the avatar — you can swap it for another face.

generate_with_gemini.py also writes the YouTube title.txt, description.txt, and tags.txt.

📝 License
This project is MIT Licensed.