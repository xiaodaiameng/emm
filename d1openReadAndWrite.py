from urllib.request import urlopen
from urllib.parse import quote  # 用于URL编码

# 对中文进行URL编码
query = quote("清华大学开源软件镜像站")


url = f"https://cn.bing.com/search?q={query}"
response = urlopen(url)

with open("myTestOpen.html", "wb") as f:
    f.write(response.read()) # 写入读取到的东西

response.close()