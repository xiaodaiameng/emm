import re
import time
from urllib.parse import unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os


TARGET_URL = "https://www.zhaopin.com/"
SAVE_DIR =r"C:\Users\Yao\Desktop\test_savedir"
save_path = os.path.join(SAVE_DIR, "finance_links00.html")
# os.makedirs(SAVE_DIR, exist_ok=True)
COOKIE_PATH = os.path.join(SAVE_DIR, "Cookies_zhaopin.txt")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def get_finance_nav_visual():
    with sync_playwright() as p:
        browser = p.chromium.launch( headless=False,slow_mo=300, executable_path=EDGE_PATH, args=["--disable-popup-blocking"])
        page = browser.new_page()
        page.set_viewport_size({"width": 400, "height": 300})
        try:
            if os.path.exists(COOKIE_PATH):
                page.goto(TARGET_URL, wait_until="domcontentloaded")
                with open(COOKIE_PATH, 'r', encoding='utf-8') as f:
                    cookies = eval(f.read())
                    page.context.add_cookies(cookies)
                page.reload(wait_until="domcontentloaded")
                print("保存的Cookie有效，跳过验证")
            else:
                cookies = page.context.cookies()
                with open(COOKIE_PATH, 'w', encoding='utf-8') as f:
                    f.write(str(cookies))
                print("Cookie已保存")

            page.wait_for_load_state("networkidle")
            page_source = page.content()
            soup = BeautifulSoup(page_source, 'html.parser')
            finance_elem = None
            finance_a = soup.find('a', string=lambda t: t and '金融' in t.strip())
            if finance_a:
                finance_elem = finance_a.find_parent('li')
                pattern = re.compile(r'<a\s+.*?href="((?!java).+?)".*?>([^<]+)</a>',re.DOTALL)
                matches = pattern.findall(str(finance_elem))
                text_set = set()
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write("""<!DOCTYPE html>
                        <html lang="zh-CN">
                        <head>
                            <meta charset="UTF-8"><title>仪表板</title><body>""")
                    for href, text in matches:
                        decoded_href = unquote(href.strip(),encoding='utf-8')
                        decoded_text = text.strip()
                        if decoded_href and decoded_text not in text_set:
                            text_set.add(decoded_text)
                            f.write(f'<a href="{decoded_href}">{decoded_text}</a><br>\n')
                    f.write(f'</body></html>\n')
                    print("="*60)
        except Exception as e:
            print(e)
        finally:
            print("操作完成，3秒后关闭浏览器...")
            time.sleep(3)
            browser.close()
    return

if __name__ == "__main__":
    get_finance_nav_visual()


    
