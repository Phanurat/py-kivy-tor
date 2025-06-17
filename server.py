from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/ipinfo')
def ip_info():
    client_ip = request.remote_addr
    try:
        resp = requests.get(f'https://ipinfo.io/{client_ip}/json')
        info = resp.json()
    except Exception:
        info = {"error": "Could not retrieve IP info"}

    return jsonify({
        "client_ip": client_ip,
        "location_info": info
    })

if __name__ == '__main__':
    app.run(port=5000)
