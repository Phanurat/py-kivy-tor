import asyncio
import requests
import logging
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# ตั้งค่า Log
logging.basicConfig(filename="tor_check.log", level=logging.DEBUG, format="%(asctime)s - %(message)s")

@app.route('/')
def home():
    return "Flask Server is Running!"

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("📥 ข้อมูลที่ได้รับ:", data)
    return jsonify({"message": "รับข้อมูลเรียบร้อย", "data": data})

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

def check_tor():
    proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }

    print("🔍 กำลังตรวจสอบการเชื่อมต่อผ่าน TOR...")
    try:
        response = requests.get('https://check.torproject.org/', proxies=proxies, timeout=10)
        ip_response = requests.get("https://api.ipify.org", proxies=proxies, timeout=10)
        ip = ip_response.text.strip()

        if "Congratulations" in response.text:
            print(f"✅ ต่อ TOR สำเร็จ\nIP: {ip}")
            logging.info(f"Connected via Tor: {ip}")
            return True
        else:
            print("❌ ยังไม่ได้เชื่อมต่อผ่าน TOR")
            logging.warning("Not using Tor.")
            return False
    except Exception as e:
        print(f"⚠️ ตรวจสอบ TOR ล้มเหลว: {e}")
        logging.error(f"Tor check failed: {e}")
        return False

async def handle_client(reader, writer):
    try:
        request = await reader.read(4096)
        header = request.decode(errors='ignore').split('\n')[0]
        method, url, _ = header.split()

        print(f"📥 {method} {url}")

        if url.startswith("http://"):
            url = url[7:]
        host = url.split('/')[0]
        path = '/' + '/'.join(url.split('/')[1:])
        port = 80

        remote_reader, remote_writer = await asyncio.open_connection(host, port)
        modified = request.replace(f"{method} http://{host}{path}".encode(), f"{method} {path}".encode())
        remote_writer.write(modified)
        await remote_writer.drain()

        while True:
            data = await remote_reader.read(4096)
            if not data:
                break
            writer.write(data)
            await writer.drain()

        remote_writer.close()
        await remote_writer.wait_closed()
    except Exception as e:
        print("❌ Error:", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def start_proxy_server():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 62881)
    print("✅ Proxy พร้อมให้บริการที่พอร์ต 62881")
    async with server:
        await server.serve_forever()

def main():
    if check_tor():
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        asyncio.run(start_proxy_server())
    else:
        print("🚫 ไม่สามารถเริ่ม Proxy ได้เพราะไม่ได้เชื่อมต่อผ่าน TOR")

if __name__ == '__main__':
    main()
