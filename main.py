import os
from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

app = Flask(__name__)

def get_fotmob_data():
    with sync_playwright() as p:
        # ใช้ chromium แบบ headless
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        stealth_sync(page)
        
        # ไปที่หน้า FotMob
        page.goto("https://www.fotmob.com/", wait_until="networkidle")
        
        # ตัวอย่าง: ดึงชื่อหัวข้อข่าวหรือชื่อหน้าเว็บ
        title = page.title()
        
        # คุณสามารถเพิ่ม logic การดึงข้อมูล (Selector) ตรงนี้ได้
        # data = page.locator(".some-class").all_text_contents()
        
        browser.close()
        return {"title": title, "status": "success"}

@app.route('/')
def home():
    return "FotMob Scraper is Running!"

@app.route('/scrape', methods=['GET'])
def scrape():
    # ตรวจสอบ API Key (เผื่อคุณตั้งไว้ใน Environment Variable เพื่อความปลอดภัย)
    api_key = request.headers.get('X-API-KEY')
    # if api_key != "YOUR_SECRET_TOKEN": return jsonify({"error": "Unauthorized"}), 403

    try:
        result = get_fotmob_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render จะกำหนด PORT มาให้ผ่าน Environment Variable ถ้าไม่มีให้ใช้ 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)