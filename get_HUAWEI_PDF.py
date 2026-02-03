# import asyncio
# import os
# from asyncio import Lock
# from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright
# import time
# from teamNeeded.zhaopinFinContent import SAVE_DIR
#
# # 目标URL
#
# TARGET_URL=("https://talent.shixizhi.huawei.com/edm3client/static/index.html?lang=zh_CN&showDownload=hide&appid=881715bf5fd14684a8e95f6a904f869e&docVersion=V1&docId=M1T9A107N1163114366272487545&oldPageNum=1&initPageNum=1&PMurl=https://talent.shixizhi.huawei.com&baseurl=https://talent.shixizhi.huawei.com/&authToken=security:25B45CF875E55C6DEF926E93:67F520AD04DAF41BF9D6009B25D4C283B55EC3D607877AA789D150136BD229C95E239A0D7D539A951EB7EFC9F45D477528D791EE685B03CC24D6EFF9763B1FF352EFA7365D4919673B1F7D7A2D74512F5451B479D8249343ECA3FF542439CCAF0A83D1D79701BC48E9CFCF6E90C63AEE382403E378343C3C01284984C9C9C9CE7622BDEA5EBE11D25A4BF83FFF9A76E92EF42FAEF0518BF5E5F838A52F8BAA23C9555D79E8B3E677F4BD0F88AF1E642A0AD495EE44BBE981FE492659B9529D1BCCD1AE9A75155C3E069FF8AEEE8088C7FFCEAD29EC105346B4178EB37987364AC8C54A72991568D3AD52DA4D663915281538E6E6845E971165D1CD7FEBA1D4337F6FC5692DDBBFF55C29B83F9812A40566D1CB22D6A6D569870B568B7CFAC5B0AC32DB2C92AFC7FB4E0F1200A6FF1720D914BAE545FA1651F9C8AC4AD6A4B98641E5C503ED47F40210453868CF0F03AEE4E3643F04A7C7F456C94C20D52AEE348AA6ED609DC8B0B941E1DDDE159FD7EC8B6512AE4114CA55F35D38FDC0DC7237584AD4041B55D513DB5CE0416802B282F52E4CA36657405F6438E2DFA4DF2B768CFB5DA258675132F55E73998DF51F9352B4A28075DC9D7CD8AF5A27981C3CBEF2D4C58B78E2846D3DA2D492EA27E77E1E6E5C4F629B31EF707C915702F1E8C5CEAA20EBB2203C1A8BC28CBFF5A5695B453535C9D33771969D7DB4FF5E6EAE7D1B61385B1E4A94207BDB8350E7EB7DD590EF460054517122D23D7D334E04B2DEECAF65854E502A27414EAC5E6B3AFCA18DD3498CD17AAEE975239619F2AEEC9A1701E658317AB9037727D6C74CF6EBC52861DCABCFD44DD1EAE6D0479A664001AC7B40731B64B193AFB086C07909FE1CD2279F303093E43A3347DC1FDC860C0D16BDEDCE81E3E10B4DEC113EC8F965064DF1D2711B846D27E48411407890DBC551A955CC5D0E9E1F8E52C6D5B51D09CD2A4896C76F2A80F9E656F10FDF709A572F3B876971271D7D0D94B831965E6359B225D2851145C2314355F700BFA3523B12D0457C536C5C3E7C1911FE905ECB2597AD7EA35D2A6B09326C6F616848EB19A3D95FD747C71A929EE6685403A98AB6818D71EE9451D066A61269E756A80180B208FD460071B1D6924C10F5F3CCF39E37FDE971798B956781673025B877A7395AF5AC460AD078C9651FB575ECACAD2849731295FB693AB0DB9DA654898932E7F4537DFD5DCFE39E51E095FA21D814B916872E89D169DDB936B1023C442BA6A52194C0D04EBF28E5B5CD9B559B7273243B056252D1AE0DE0C8720F5C0971CC5B2F5433E9A8E3C198F3B88492F577D7287F6832BB4E84D1EB83C3CA3D3D9F2B1F225D1DCFFDCDF1C8CE01858270A88808C7B1B43E57C9B489260DDB876C5BBABB1518D522DCD453EB5C0B0A7A7696ED99352E0607EDBD8A1C4477B5D87BA3FD33686F12674B324A26D2AD44697CEF52318A44C554014A59067A12A72265027946A79FE1281ADCE25CBD4D1515454B82B33D84B56A941F31B983882E1FFE76C79EA510ACFB19AF0267AEBE4938A8F975C87634E794074B094DA8E5616FF95057BACE0C5FA4196EDADA06FB79C2414E08315CBF08&jslibhtml=https://talent.shixizhi.huawei.com/edm3client/static/index.html?lang=zh_CN&lang=zh_CN&type=doc&pageNum=1&#/")
# EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
# SAVE_DIR = r"D:\PythonCode\PyCrawler\small_project\personalTest\Imgs"
#
# def save_huawei_blob_images(target_url, edge_browser_path, save_dir):
#     image_count = 0
#     processed_blob_urls = set()  # 去重集合
#
#     # 创建保存目录
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
#     print(f"✅ 初始化完成：图片将保存到 {save_dir}")
#     print(f"✅ 目标页面：{target_url[:60]}...\n")
#
#     with sync_playwright() as p:
#         # 启动浏览器（保留界面方便观察）
#         browser = p.chromium.launch(
#             headless=False,
#             executable_path=edge_browser_path,
#             args=["--disable-popup-blocking", "--disable-web-security"]
#         )
#         page = browser.new_page()
#
#         # 监听图片响应并保存
#         def handle_image_response(response):
#             nonlocal image_count
#             request_url = response.request.url
#             # 只处理未保存过的有效blob图片
#             if "blob:" in request_url and response.ok and request_url not in processed_blob_urls:
#                 try:
#                     processed_blob_urls.add(request_url)
#                     image_count += 1
#                     # 保存图片
#                     image_data = response.body()
#                     img_path = os.path.join(save_dir, f"Huawei_Blob_Img_{image_count}.png")
#                     with open(img_path, "wb") as f:
#                         f.write(image_data)
#                     print(f"✅ 已保存 [第{image_count}张]：{img_path}")
#                 except Exception as e:
#                     print(f"❌ 保存失败（{request_url[:50]}...）：{str(e)}")
#
#         page.on("response", handle_image_response)
#
#         try:
#             # 加载页面
#             print("🔄 正在加载页面...")
#             page.goto(target_url, wait_until="networkidle")
#             print("✅ 页面初始加载完成，开始滚动加载更多图片...\n")
#
#             # 核心修改：适配独立滚动容器 + 延长等待 + 调整停止条件
#             max_scrolls = 200  # 足够大的滚动次数
#             scroll_pause_time = 7  # 每次滚动后等待3秒（给图片加载时间）
#             scroll_step = 500  # 每次滚动500像素（模拟渐进式滚动）
#             last_image_count = 0
#             no_new_image_count = 0  # 连续无新图片的次数
#
#             for scroll_count in range(1, max_scrolls + 1):
#                 # 模拟渐进式滚动（更接近用户行为，触发懒加载）
#                 # 先获取当前滚动位置，再滚动500像素
#                 current_scroll = page.evaluate("window.scrollY")
#                 page.evaluate(f"window.scrollTo(0, {current_scroll + scroll_step});")
#                 print(f"📜 正在滚动（{scroll_count}/{max_scrolls}次），当前位置：{current_scroll + scroll_step}px")
#                 time.sleep(scroll_pause_time)  # 延长等待时间
#
#                 # 检查是否有新图片加载（用图片数量判断，而非页面高度）
#                 if image_count > last_image_count:
#                     last_image_count = image_count
#                     no_new_image_count = 0  # 有新图片，重置计数器
#                 else:
#                     no_new_image_count += 1
#                     print(f"⚠️  未检测到新图片（连续{no_new_image_count}次）")
#
#                 # 停止条件：连续5次无新图片，说明已加载完
#                 if no_new_image_count >= 10:
#                     print("✅ 连续无新图片，停止滚动")
#                     break
#
#             # 滚动结束后，额外等待5秒让剩余图片加载
#             print("\n⌛ 滚动结束，等待剩余图片加载...")
#             time.sleep(9)
#
#             # 校验图片数量
#             page_blob_urls = page.evaluate('''() => {
#                 return Array.from(document.querySelectorAll('img[src^="blob:"]')).map(img => img.src);
#             }''')
#             total_blob = len(page_blob_urls)
#             saved_blob = image_count
#
#             print(f"\n✅ 校验结果：")
#             print(f"   - 页面中实际存在 {total_blob} 个blob图片")
#             print(f"   - 已成功保存 {saved_blob} 个blob图片")
#             if saved_blob < total_blob:
#                 print(f"⚠️  建议：增加scroll_pause_time（如改为4秒）或max_scrolls（如200）")
#
#         except Exception as e:
#             print(f"\n❌ 操作失败：{str(e)}")
#             print("   请检查URL、浏览器路径及网络")
#
#         finally:
#             browser.close()
#             print(f"\n" + "="*60)
#             print(f"📊 任务结束：共保存 {image_count} 张图片")
#             print(f"📂 保存位置：{save_dir}")
#             print("="*60)
#
#
# if __name__ == "__main__":
#     save_huawei_blob_images(TARGET_URL, EDGE_PATH, SAVE_DIR)