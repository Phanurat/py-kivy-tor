from kivy.app import App
from kivy.uix.button import Button
import requests

class TorApp(App):
    def build(self):
        btn = Button(text="Check Tor Connection")
        btn.bind(on_press=self.check_tor)
        return btn

    def check_tor(self, instance):
        proxies = {
            'http': 'socks5h://127.0.0.1:9150',
            'https': 'socks5h://127.0.0.1:9150'
        }
        try:
            response = requests.get('https://check.torproject.org/', proxies=proxies, timeout=10)
            if "Congratulations" in response.text:
                instance.text = "Connected via Tor!"
            else:
                instance.text = "Not using Tor."
        except Exception as e:
            instance.text = f"Error: {e}"

if __name__ == '__main__':
    TorApp().run()
