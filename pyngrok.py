from pyngrok import ngrok

public_url = ngrok.connect(5000)
print("🌍 เข้าผ่าน URL นี้ได้:", public_url)
