from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def scrape_fotmob():
    with sync_playwright() as p:
        # ใช้ chromium แบบ headless
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # ใช้ stealth เพื่อไม่ให้โดนบล็อก
        stealth_sync(page)
        
        page.goto("https://www.fotmob.com/", wait_until="networkidle")
        print(f"Title: {page.title()}")
        
        # ดึงข้อมูลที่ต้องการที่นี่...
        
        browser.close()

if __name__ == "__main__":
    scrape_fotmob()