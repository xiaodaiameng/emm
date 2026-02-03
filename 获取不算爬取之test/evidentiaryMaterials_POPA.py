import requests
import os

path = r"C:\Users\ass\Desktop\popa.txt"
save_dir = r"C:\Users\ass\Desktop\runningImgs"  # 明确定义保存路径

# 创建保存文件夹（重要！）
os.makedirs(save_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

with open(path, 'r', encoding='utf-8') as file:
    list01 = [line.strip() for line in file.readlines() if line.strip()]  # 过滤空行
    
    for perUrl in list01:
        # 从 URL 参数中提取原始文件名（正确方法）
        if 'filename=' in perUrl:
            # 找到 filename= 后面的部分
            filename_start = perUrl.find('filename=') + 9
            # 找到下一个 & 或结尾
            filename_end = perUrl.find('&', filename_start)
            if filename_end == -1:
                img_name = perUrl[filename_start:]
            else:
                img_name = perUrl[filename_start:filename_end]
        else:
            # 备选方案：使用 URL 路径最后一部分
            img_name = perUrl.split('/')[-1].split('?')[0]
        
        # 解码 URL 编码的文件名
        import urllib.parse
        img_name = urllib.parse.unquote(img_name)
        
        # 完整的保存路径
        save_path = os.path.join(save_dir, img_name)
        
        response = requests.get(perUrl, headers=headers, timeout=30)
        with open(save_path, "wb") as f:
            f.write(response.content)
            print(f"下载完成: {img_name}")
print("——————————————————")