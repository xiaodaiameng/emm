# 找到 m3u8（用尽各种手段）
# 通过 m3u8下载到 ts文件
# 把 ts文件合并为一个 mp4文件

找 m3u8 首先网页没有，从 标签 vedio的{url} 找起，正是.m3u8文件。
复制 url 直接审查元素 Headers, 在正确Name文件找到其 Headers的 Request URL（上面那个），
点到 Preview看各种信息和加密公式或者看得见 .ts文件

需要刷新——因为发现某个元素导致内部网址的内部元素变化，即他对每一个这个字符串做了一个时效性的检测——反爬机制

结合正则，
obj = re.compile(r"url:'(?P<url>.*?)',",re.S)
m3u8_url = obj.search(resp.text).group("url")
print(m3u8_url)
resp.close()
下载该网址的解析式（那些公式和 ts文件）
resp2=requests.get(m3u8_url, headers=headers)
n = 1
with open("哲仁王后.m3u8", mode="wb") as f:
    # f.write(resp2.content)
    更精的筛选：
    for line in f:
        line = line.strip() # 去掉空格，空白，换行符
        if line.startswith("#"):# 如果以#开头，我不需要，跳过继续
            continue
        resp3 = requests.get(line)
        f = open(f"{n}.ts", mode = "wb")
        f.write(resp3.content)
        n += 1
resp2.close()

resp = requests.get(url)
main_page = BeautifulSoup(resp.text, "html.parser")
src = main_page.find("iframe").get("src")


下载视频，下载秘钥，进行解密操作，合并所有ts文件为一个mp4文件