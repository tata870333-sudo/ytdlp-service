import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "YT-DLP Service is running!"

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json() or {}
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'extractor_args': {'youtube': {'player_client': ['android']}}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info.get('url'),
                'ext': info.get('ext')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
