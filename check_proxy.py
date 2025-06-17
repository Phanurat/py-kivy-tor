import requests

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

try:
    r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
    print("🟢 Success:", r.json())
except Exception as e:
    print("🔴 Failed:", e)
