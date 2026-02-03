import time
import requests
from bs4 import BeautifulSoup

url = "https://www.nasachina.cn/astronomy-picture-of-the-day"  # NASA每日天文一图

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Referer": "https://www.nasachina.cn/"
}
response = requests.get(url, headers=headers)
download_count = 0
# 增加主页面请求状态判断
if response.status_code == 200:
    page = BeautifulSoup(response.text, "html.parser")
    alist = page.find_all("a", attrs={"class": "elementor-post__thumbnail__link"})
    # print(f"共找到 {len(alist)} 个符合条件的链接，此处仅打印 href ，不打印标签属性和图片src。")

    for i, a_tag in enumerate(alist, 1):
            print(f"--- 第 {i} 个链接 ---")
            href = a_tag.get("href")
            # print(f"链接地址: {href}")
            if href and href.startswith(('http://', 'https://')):  # 更严谨的URL检查
                try:
                    print("正在请求子页面...")
                    time.sleep(1)
                    child_page_response = requests.get(href)
                    child_page_response.encoding = 'utf-8'

                    if child_page_response.status_code == 200:
                        child_page = BeautifulSoup(child_page_response.text, "html.parser")
                        target_a = None
                        target_img = None
                        for a_tag in child_page.find_all("a", href=True):

    # 算了，我妥协了，我不拿那个高清的href的图片地址了，我拿那个a包裹的 < img src = > 的 src的地址
                            # 同时检查是否包含img和.jpg结尾
                        #     if a_tag.find("img") and a_tag.get("href", "").lower().endswith(".jpg"):
                        #         target_a = a_tag
                        #         break
                        # if target_a:
                        #     high_res_href = target_a.get("href")
                        #     print(f"子页面完整图片URL: {high_res_href}\n")
                        # 改为
                            img_tag = a_tag.find("img")  # 提取a标签内部的img标签
                            if img_tag and img_tag.get("src", "").lower().endswith(".jpg"):  # 确保img的src是jpg
                                target_img = img_tag
                                break
                        if target_img:
                            # 提取img标签的src属性（这就是你要的显示图地址）
                            img_src = target_img.get("src")
                            print(f"子页面img标签的src地址: {img_src}")
            # 下载图片
            #                 img_response = requests.get(img_src, headers=headers)
            #                 img_name = img_src.split("/")[-1]  # 拿到url中的最后一个/以后的内容
            #                 with open(f"Imgs/NASA_imgs/{img_name}", "wb") as f:
            #                     f.write(img_response.content)
            #                 print("over:", img_name)
                            download_count += 1
                            time.sleep(1)
                            if download_count >= 10:
                                print("已完成 10 次下载，终止循环")
                                break
                        else:
                            print("子页面中未找到包含.jpg的图片链接\n")
                    else:
                        print(f"子页面请求失败，状态码: {child_page_response.status_code}\n")

                except Exception as e:
                    print(f"处理子页面时出错: {str(e)}\n")
            else:
                print("无效的链接地址，跳过请求\n")
            if download_count >= 10:
                break
else:
    print(f"主页面请求失败，状态码: {response.status_code}")

f.close()
print("allover——————————————————")


#
# https://www.nasachina.cn/wp-content/uploads/2025/09/StarTrailsOne-MileRadioTelescope    2100.jpg
# https://www.nasachina.cn/wp-content/uploads/2025/09/StarTrailsOne-MileRadioTelescope    1050-768x512.jpg
#
