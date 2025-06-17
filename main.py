from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests

class TorIPLocationApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text="Press Refresh to get IP & Location via Tor", halign='center')
        self.btn = Button(text="Refresh")
        self.btn.bind(on_press=self.refresh_info)

        layout.add_widget(self.label)
        layout.add_widget(self.btn)
        return layout

    def refresh_info(self, instance):
        proxies = {
            'http': 'socks5h://127.0.0.1:9150',
            'https': 'socks5h://127.0.0.1:9150'
        }

        # เปลี่ยน URL เป็น .onion server ของคุณ (http, ไม่ต้อง https)
        onion_url = 'http://youronionaddress.onion/api/ipinfo'

        try:
            response = requests.get(onion_url, proxies=proxies, timeout=15)
            response.raise_for_status()
            data = response.json()

            ip = data.get("client_ip", "Unknown IP")
            location = data.get("location_info", {})
            city = location.get("city", "Unknown city")
            region = location.get("region", "Unknown region")
            country = location.get("country", "Unknown country")

            self.label.text = f"IP: {ip}\nLocation: {city}, {region}, {country}"
        except Exception as e:
            self.label.text = f"Error:\n{e}"

if __name__ == '__main__':
    TorIPLocationApp().run()
