from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import requests
import subprocess
import logging

# ตั้งค่า Log
logging.basicConfig(filename="tor_check.log", level=logging.DEBUG, format="%(asctime)s - %(message)s")

class TorTool(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.status_label = Label(text="🔍 ตรวจสอบการเชื่อมต่อผ่าน TOR", font_size=18, size_hint=(1, 0.1))
        self.add_widget(self.status_label)

        # ปุ่มตรวจสอบ TOR
        self.check_btn = Button(text="🔗 Check TOR Connection", size_hint=(1, 0.2), font_size=16)
        self.check_btn.bind(on_press=self.check_tor)
        self.add_widget(self.check_btn)

        # ช่องพิมพ์ Website
        self.website_input = TextInput(text="example.com", hint_text="ใส่เว็บไซต์ที่ต้องการ ping เช่น google.com", size_hint=(1, 0.1), multiline=False)
        self.add_widget(self.website_input)

        # ปุ่ม Ping
        self.ping_btn = Button(text="📡 Ping Website", size_hint=(1, 0.2), font_size=16)
        self.ping_btn.bind(on_press=self.ping_website)
        self.add_widget(self.ping_btn)

        # ช่องแสดงผลลัพธ์
        self.output_label = Label(text="📄 Output:", size_hint=(1, 0.1))
        self.add_widget(self.output_label)

        self.output = TextInput(text="", readonly=True, size_hint=(1, 0.4), font_size=14)
        self.add_widget(self.output)

    def check_tor(self, instance):
        proxies = {
            'http': 'socks5h://127.0.0.1:9150',
            'https': 'socks5h://127.0.0.1:9150'
        }

        try:
            response = requests.get('https://check.torproject.org/', proxies=proxies, timeout=10)
            ip_response = requests.get("https://api.ipify.org", proxies=proxies, timeout=10)
            ip = ip_response.text.strip()

            if "Congratulations" in response.text:
                self.status_label.text = f"✅ ผ่าน TOR\nIP: {ip}"
                self.check_btn.text = "✔ Connected via Tor"
                logging.info(f"Connected via Tor: {ip}")
            else:
                self.status_label.text = "❌ ไม่ได้ใช้ TOR"
                logging.warning("Not using Tor.")
        except Exception as e:
            self.status_label.text = f"⚠️ Error: {e}"
            logging.error(f"Tor check failed: {e}")

    def ping_website(self, instance):
        website = self.website_input.text.strip()
        if not website:
            self.output.text = "❌ กรุณาใส่ชื่อเว็บไซต์ก่อน"
            return

        try:
            # ใช้ ping เหมือน CMD
            result = subprocess.run(["ping", website, "-n", "4"], capture_output=True, text=True, shell=True)
            self.output.text = result.stdout
            logging.info(f"Ping {website}:\n{result.stdout}")
        except Exception as e:
            self.output.text = f"⚠️ Ping error: {e}"
            logging.error(f"Ping failed: {e}")

class TorApp(App):
    def build(self):
        return TorTool()

if __name__ == '__main__':
    TorApp().run()
