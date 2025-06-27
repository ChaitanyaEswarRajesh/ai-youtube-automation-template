import os
import webbrowser
import requests
from urllib.parse import urlencode, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

# Replace with your client_id and client_secret before running or use env vars
CLIENT_ID = os.getenv("YT_CLIENT_ID") or "YOUR_CLIENT_ID"
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET") or "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "https://www.googleapis.com/auth/youtube.upload"

# Step 1: Authorize in browser
params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": SCOPE,
    "access_type": "offline",
    "prompt": "consent"
}
auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
print("🔗 Open the following URL in your browser to authorize:\n")
print(auth_url)
webbrowser.open(auth_url)

# Step 2: Handle redirect with code
class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = self.path.split("?")[-1]
        params = parse_qs(query)
        code = params.get("code", [None])[0]

        if code:
            print(f"✅ Authorization code received: {code}")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>You can close this tab now.</h1>")

            # Step 3: Exchange code for tokens
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code"
            }
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                tokens = response.json()
                print(f"🎉 REFRESH TOKEN: {tokens['refresh_token']}")
            else:
                print("❌ Error getting token:", response.text)

        else:
            self.send_error(400, "Missing code")

server = HTTPServer(("localhost", 8080), OAuthHandler)
print("🌐 Waiting for authorization code on http://localhost:8080 ...")
server.handle_request()
