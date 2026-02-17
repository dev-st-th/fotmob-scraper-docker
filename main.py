import os
from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def get_fotmob_data(target_url):
    with sync_playwright() as p:
        # เปิด Browser แบบไม่ต้องใช้ Stealth ก่อน เพื่อให้รันผ่านชัวร์ๆ
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # ไปยัง URL ที่ส่งมาจาก Worker
        page.goto(target_url, wait_until="networkidle")
        
        # ดึงข้อความ JSON จากหน้าเว็บ (FotMob API จะแสดงผลเป็น text ในหน้าจอ)
        content = page.locator("body").inner_text()
        
        browser.close()
        return content

@app.route('/')
def home():
    return "FotMob Scraper is Live and Ready!"

@app.route('/scrape', methods=['GET'])
def scrape():
    # รับ URL จาก Cloudflare Worker ผ่าน parameter ?url=...
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Please provide a URL"}), 400

    try:
        data = get_fotmob_data(url)
        return data, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # สำคัญ: Render บังคับให้ใช้ Port ที่เขากำหนดให้
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)