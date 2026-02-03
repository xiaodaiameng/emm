import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# ---------------------- 配置参数 ----------------------
# 目标网站URL
TARGET_URL = "http://www.yinhangzhaopin.com/"

# 数据保存路径（TXT文件）
DATA_SAVE_PATH = os.path.join(r"D:\PythonCode\PyCrawler\small_project\Comments\JobWeb", "bank_recruitment_links.txt")


# ---------------------- 获取页面HTML ----------------------
def get_page_html():
    """使用Playwright获取页面完整HTML内容"""
    try:
        with sync_playwright() as p:
            # 启动浏览器（headless=False可显示界面调试）
            browser = p.chromium.launch(headless=False, channel="chrome")
            page = browser.new_page()

            # 访问目标页面
            page.goto(TARGET_URL, wait_until="networkidle")
            page.wait_for_timeout(1000)  # 等待页面完全加载

            # 获取页面HTML
            page_html = page.content()
            browser.close()
            print("✅ 成功获取页面HTML")
            return page_html
    except Exception as e:
        print(f"❌ 获取页面失败：{str(e)}")
        return None


# ---------------------- 解析页面信息 ----------------------
def parse_bank_info(page_html):
    """解析HTML，提取目标区域的链接和标题"""
    if not page_html:
        return []

    soup = BeautifulSoup(page_html, "lxml")
    result_list = []

    # 定位目标容器
    target_container = soup.find("div", class_="yhksw_bankAd")
    if not target_container:
        print("❌ 未找到目标容器div.yhksw_bankAd")
        return []

    # 提取所有图片链接项
    items = target_container.find_all("div", class_="imagesdiv yhzpw_index_sec")
    if not items:
        print("❌ 未找到任何广告项")
        return []

    # 循环提取每个项的信息
    for idx, item in enumerate(items, 1):
        try:
            # 提取链接
            link_tag = item.find("a")
            href = link_tag.get("href", "") if link_tag else ""

            # 提取标题（从img的alt属性获取）
            img_tag = item.find("img")
            title = img_tag.get("alt", "") if img_tag else ""

            # 提取图片URL
            img_url = img_tag.get("src", "") if img_tag else ""

            # 保存信息
            result_list.append({
                "序号": idx,
                "标题": title,
                "链接": href,
                "图片URL": img_url
            })
            print(f"✅ 提取第{idx}条信息：{title}")
        except Exception as e:
            print(f"❌ 提取第{idx}条信息失败：{str(e)}")
            continue

    return result_list


# ---------------------- 保存数据到TXT ----------------------
def save_to_txt(data_list):
    """将提取的信息保存到TXT文件"""
    if not data_list:
        print("❌ 无数据可保存")
        return

    try:
        with open(DATA_SAVE_PATH, "w", encoding="utf-8") as f:
            f.write("银行招聘信息汇总\n")
            f.write("=" * 50 + "\n\n")

            for item in data_list:
                f.write(f"序号：{item['序号']}\n")
                f.write(f"标题：{item['标题']}\n")
                f.write(f"链接：{item['链接']}\n")
                f.write(f"图片：{item['图片URL']}\n")
                f.write("-" * 50 + "\n")

        print(f"✅ 数据已保存到：{DATA_SAVE_PATH}")
    except Exception as e:
        print(f"❌ 保存数据失败：{str(e)}")


# ---------------------- 主函数 ----------------------
def main():
    print("===== 开始爬取银行招聘网信息 =====")
    # 1. 获取页面HTML
    page_html = get_page_html()
    if not page_html:
        return

    # 2. 解析信息
    bank_info = parse_bank_info(page_html)
    if not bank_info:
        return

    # 3. 保存到TXT
    save_to_txt(bank_info)
    print("===== 爬取流程全部完成 =====")


if __name__ == "__main__":
    main()
