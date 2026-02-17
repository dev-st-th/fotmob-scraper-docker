import os
import time
from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync # ลองกลับมาใช้ตัวนี้อีกครั้ง

app = Flask(__name__)

def get_fotmob_data(target_url):
    with sync_playwright() as p:
        # ใช้ Browser ตัวเต็ม (ไม่ใช้ headless-shell) เพื่อลดโอกาสโดนตรวจจับ
        browser = p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled"
        ])
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        
        # ใช้ Stealth เพื่อพรางตัวว่าเป็นคนจริงๆ
        try:
            stealth_sync(page)
        except:
            pass # ถ้ายัง import มีปัญหา ให้ข้ามไปก่อน
            
        # ไปที่หน้าเว็บหลักของ FotMob ก่อนหนึ่งรอบเพื่อสร้าง Cookie
        page.goto("https://www.fotmob.com/", wait_until="networkidle")
        time.sleep(2) # รอสักครู่ให้คุกกี้เซ็ตตัว
        
        # ค่อยไปที่ URL เป้าหมาย
        page.goto(target_url, wait_until="networkidle")
        
        # ดึงเนื้อหา
        content = page.locator("body").inner_text()
        
        browser.close()
        return content

@app.route('/')
def home():
    return "FotMob Scraper is Active"

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL"}), 400
    try:
        data = get_fotmob_data(url)
        return data, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)