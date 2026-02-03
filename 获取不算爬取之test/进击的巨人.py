
url = "https://v.qq.com/x/cover/mzc00200whsp9r6/a0047l69jnp.html"
target_vedio = "https://v.qq.com/wasm-kernel/1.0.49/fake-video-element-iframe.js?max_age=86400"
SAVE_DIR = r"D:\Codes\py\Crawler\chinese\vedio"
SAVE_PATH = os.path.join(SAVE_DIR, "fanhua.mp4")



from playwright.sync import sync_playwright # synchronize
import requests
import time


def download_video(url, save_path="video.mp4"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.on("response", handle_response)
        page.goto(url)
        page.wait_for_selector("video", state="visible")
        time.sleep(5)
        browser.close()
        if video_url:
            print(f"开始下载视频到 {save_path}...")
            response = requests.get(video_url, stream=True)
            with open(save_path, "wb") as f:
                cnt = 0
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB 块
                    if chunk:
                        f.write(chunk)
                        cnt += 1
                        if cnt == 10:
                            break
            print("已下载十个块")
        else:
            print("未捕获到视频地址，请检查页面是否正确或延长等待时间。")

download_blob_video(video_url, save_path="SAVE_PATH")


