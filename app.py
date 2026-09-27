import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
API_URL = 'https://musicfab.io/api/spotify'

@app.get('/')
def home():
    return render_template('index.html')

@app.post('/api/song')
def song():
    data = request.get_json(silent=True) or {}
    url = str(data.get('url', '')).strip()
    if not url.startswith(('https://open.spotify.com/track/', 'https://spotify.link/')):
        return jsonify(error='Please enter a Spotify track link.'), 400
    try:
        response = requests.post(API_URL, json={'url': url}, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.Timeout:
        return jsonify(error='API timed out. Try again.'), 504
    except requests.RequestException:
        return jsonify(error='Upstream API failed. Try again later.'), 502
    except ValueError:
        return jsonify(error='API returned invalid JSON.'), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')))
