import requests
import ipaddress

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

def get_public_ip():
    try:
        ip = requests.get("https://ipv4.icanhazip.com/", proxies=proxies, timeout=10).text.strip()
        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_private:
            print(f"❌ ได้ IP {ip} แต่เป็น Private IP (ไม่ใช่ Public)")
        elif ip_obj.is_loopback:
            print(f"❌ ได้ IP {ip} แต่เป็น Loopback")
        elif ip_obj.is_global:
            print(f"✅ ได้ IP สาธารณะ (Public IP): {ip}")
        else:
            print(f"⚠️ ได้ IP ที่ไม่ใช่ Public: {ip}")
    except Exception as e:
        print(f"⚠️ ดึง IP ไม่สำเร็จ: {e}")

get_public_ip()
