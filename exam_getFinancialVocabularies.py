import time
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import unquote

url = "https://wiki.mbalib.com/wiki"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "Referer": "https://wiki.mbalib.com/"
}


save_dir = "../Comments/FinancialVocabularies"
# os.makedirs(save_dir, exist_ok=True)# 创建保存目录（如果不存在）

response = requests.get(url, headers=headers)

# 增加主页面请求状态判断
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # 1. 先找到所有表格行<tr>，再遍历每行中的单元格<td>
    rows = soup.find_all('tr')  # 获取所有表格行
    for row_idx, row in enumerate(rows, 1):
        # 2. 获取当前行中的所有单元格<td>
        tds = row.find_all('td')
        for td_idx, td in enumerate(tds, 1):
            # 为每个td设置独立计数器，最多下载3个
            td_download_count = 0
            if 'style' in td.attrs and 'line-height:180%' in td['style']:
                a_tags = td.find_all('a')
                if a_tags:
                    print(f"\n第{row_idx}行，第{td_idx}列的td内容：")
                    for a in a_tags:
                        # 如果当前td已下载3个，跳到下一个td
                        if td_download_count >= 3:
                            print(f"当前td已下载3个文件，开始处理下一个td")
                            break

                        text = a.get_text()
                        link = a.get('href')
                        # 检查link是否存在
                        if not link:
                            print(f"跳过无链接的{a.text}")
                            continue

                        full_link = 'https://wiki.mbalib.com/' + link

                        try:
                            # 添加延迟，避免请求过于频繁
                            time.sleep(1)

                            child_response = requests.get(full_link, headers=headers)
                            if child_response.status_code != 200:
                                print(f"请求失败，状态码：{child_response.status_code}")
                                continue

                            child_soup = BeautifulSoup(child_response.text, 'html.parser')
                            # 查找包含子链接的元素
                            catmore_div = child_soup.find('div', attrs={"class": "boilerplate", "id": "catmore"})
                            if not catmore_div:
                                print("未找到catmorediv")
                                continue

                            # 从div中查找a标签获取链接
                            grand_a_tag = catmore_div.find('a')
                            if not grand_a_tag:
                                print("catmorediv中未找到a标签")
                                continue

                            grand_href = grand_a_tag.get('href')
                            if not grand_href:
                                print("a标签中未找到href属性")
                                continue
                            # 处理相对路径
                            if grand_href.startswith('/'):
                                grand_href = 'https://wiki.mbalib.com' + grand_href
                            elif not grand_href.startswith('http'):
                                grand_href = 'https://wiki.mbalib.com/wiki/' + grand_href

                            encoded_soup_name = grand_href.split("/")[-1]
                            decoded_soup_name = unquote(encoded_soup_name, encoding='utf-8')
                            if not decoded_soup_name.endswith(".html"):
                                decoded_soup_name += ".html"

                            # 添加延迟
                            time.sleep(1)

                            grand_response = requests.get(grand_href, headers=headers)
                            if grand_response.status_code != 200:
                                print(f"下载失败，状态码：{grand_response.status_code}")
                                continue

                            save_path = os.path.join(save_dir, decoded_soup_name)
                            # if not os.path.exists(save_path):
                                # with open(save_path, "wb") as f:
                                #     f.write(grand_response.content)
                                #     td_download_count += 1
                                #     print(f"当前td已下载 {td_download_count}/3: {decoded_soup_name}")
                            # else:
                            #     print(f"文件已存在，跳过下载: {decoded_soup_name}")

                        except Exception as e:
                            print(f"处理过程出错：{str(e)}")
                            continue

    print("所有链接处理完毕")
else:
    print(f"主页面请求失败，状态码：{response.status_code}")
