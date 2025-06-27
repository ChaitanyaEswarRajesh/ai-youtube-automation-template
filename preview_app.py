from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)
OUTPUT_DIR = 'output'

@app.route('/')
def index():
    videos = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp4')]
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Preview</title>
    </head>
    <body>
        <h1>Generated Videos</h1>
        {% for video in videos %}
            <div>
                <h3>{{ video }}</h3>
                <video width="480" controls>
                    <source src="/video/{{ video }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        {% endfor %}
    </body>
    </html>
    """, videos=videos)

@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
