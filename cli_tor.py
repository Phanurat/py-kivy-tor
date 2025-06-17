import requests
import subprocess
import logging

# ตั้งค่า Log
logging.basicConfig(filename="tor_check.log", level=logging.DEBUG, format="%(asctime)s - %(message)s")

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
        else:
            print("❌ ยังไม่ได้เชื่อมต่อผ่าน TOR")
            logging.warning("Not using Tor.")
    except Exception as e:
        print(f"⚠️ ตรวจสอบ TOR ล้มเหลว: {e}")
        logging.error(f"Tor check failed: {e}")

def ping_website(website):
    website = website.strip()
    if not website:
        print("❌ กรุณาใส่ชื่อเว็บไซต์")
        return

    try:
        print(f"📡 Ping เว็บไซต์ {website} ...")
        result = subprocess.run(["ping", website, "-n", "4"], capture_output=True, text=True, shell=True)
        print(result.stdout)
        logging.info(f"Ping {website}:\n{result.stdout}")
    except Exception as e:
        print(f"⚠️ Ping error: {e}")
        logging.error(f"Ping failed: {e}")

if __name__ == '__main__':
    print("==== TOR TOOL CLI ====")
    check_tor()

    while True:
        site = input("🌐 พิมพ์ชื่อเว็บไซต์ที่ต้องการ Ping (หรือพิมพ์ 'exit' เพื่อออก): ")
        if site.lower() == "exit":
            print("👋 ออกจากโปรแกรมแล้ว")
            break
        ping_website(site)
