
# /html/body/div/div/div[2]/div[1]/div[1]
#
# <div class="head-img"
# style=("background-image: "
#        "url(&quot;https://s3gw.cmbimg.com/sc/JonWtH3SmRv7WFuP1lJ3SUn0GCs=/SZ::"
#        "ZnQ3YzJfaM7bQJjuEjZjYRZz&quot;);")>
# </div>
import playwright.sync_api as playwright
import os

# ---------------------- 1. 配置基础信息 ----------------------
target_url = "https://career.cmbchina.com/campus/home"  # 目标网页
SAVE_DIR = r"D:\PythonCode\PyCrawler\small_project\Comments\JobWeb"
save_html_path = os.path.join(SAVE_DIR, "bankImg.html")
jump_link = "https://career.cmbchina.com/campus/recruit"  # 点击跳转链接


# ---------------------- 2. 用 Playwright 启动浏览器并提取元素 ----------------------
def get_target_image_info():
    try:
        with playwright.sync_playwright() as p:
            # 使用Edge浏览器通道（基于Chromium）
            browser = p.chromium.launch(
                headless=False,  # 显示浏览器界面
                channel="msedge"
            )
            page = browser.new_page()

            # 打开目标网页
            page.goto(target_url)

            # 等待目标元素加载（最多等待10秒）
            head_img_div = page.wait_for_selector("div.head-img", timeout=10000)

            if not head_img_div:
                print("❌ 未找到目标图片元素（div.head-img）")
                browser.close()
                return None, None

            # 提取 style 属性
            style_attr = head_img_div.get_attribute("style")


            if not style_attr:
                print("❌ 目标元素的 style 属性为空")
                browser.close()
                return None, None

            # 提取背景图片 URL
            img_url = None


            match_quote = page.evaluate(
                r"""
                (style) => {
                    const match = style.match(/url\("([^"]+)"\)/);
                    return match ? match[1] : null;
                }
                """,
                style_attr
            )
            img_url = match_escape or match_quote

            if not img_url:
                print(f"❌ 未从 style 属性中提取到图片 URL，style 内容：{style_attr[:100]}...")
                browser.close()
                return None, None

            print(f"✅ 成功提取图片 URL：{img_url}")
            browser.close()
            return img_url, jump_link

    except Exception as e:
        print(f"❌ 爬取过程出错：{str(e)}")
        return None, None


# ---------------------- 3. 生成自定义 HTML 文件 ----------------------
def generate_custom_html(img_url, jump_link):
    if not img_url or not jump_link:
        print("❌ 缺少图片URL或跳转链接，无法生成HTML")
        return
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>招商银行校园招聘</title>
</head>
<body>
    <div style="width: 1600px; height: 500px; overflow: auto;  margin-left: auto">
        <a href="{jump_link}" target="_blank">
            <img src="{img_url}" alt="招商银行校园招聘Banner，点击跳转招行官网">
        </a>
        <p style="text-align: right; margin-right: calc((100% - 1600px) / 2); margin-top: 8px; color: #666;">
            提示：点击图片可跳转至招行官网招聘页面
        </p>
    </div>
    
</body>
</html>'''

    # 2. 写入HTML文件（核心修复：写入生成好的 html_content）
    try:
        with open(save_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)  # 直接写入完整的HTML内容
        print(f"🔍 生成的文件路径（可直接复制打开）：{os.path.abspath(save_html_path)}")
    except Exception as e:
        print(f"❌ 生成 HTML 文件出错：{str(e)}")


# ---------------------- 4. 执行主逻辑 ----------------------
if __name__ == "__main__":
    # 确保浏览器已安装（低版本Playwright需要手动安装）
    print("⚠️ 请确保已执行以下命令安装Edge浏览器支持：")
    print("set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/")
    print("playwright install msedge")

    img_url, jump_link = get_target_image_info()
    generate_custom_html(img_url, jump_link)

# html_str = ('        <!----></a></li></ul>')
#当页面源代码不换行时，
# tag_pattern = re.compile(r'<[^>]+>')  # 匹配所有HTML标签
# # 用sub方法：找到每个标签，在标签后添加 <br>\n（换行）
# formatted_html = tag_pattern.sub(lambda m: m.group() + '<br>\n', html_str)
#
# # 5. 增加调试：打印匹配到的内容长度和前200字符（确认有内容）
# print(f"🔍 匹配到的内容长度：{len(formatted_html)} 字符")
# print(f"📄 内容预览（前200字符）：\n{formatted_html[:200]}")
