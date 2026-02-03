
url = "https://www.bilibili.com/video/BV1a1421Z7DZ?t=9.0"



headers = {
    UA
}
resp = requests.get(videoStatusUrl, headers=headers)
print(resp.text)# 显示该文章已下架，可能是防盗链问题 1 》 2 》 3    他会回溯查找 1，2 的身份，找 headers里的 refer 的 url复制进 headers的字典

# 然后
dict = resp.json()
# 根据实际情况
srcUrl = dict['videoInfo']['videos']['srcUrl']
# 在 preview里找 systemTime 复制
systemTime = dic['systemTime']
srcUrl = srcUrl.replace(systemTime, f"cont-{contId}")
print(srcUrl)

# 下载视频，记得 pycharm 排除对它的索引，reveal in finders
# with open(srcUrl, "wb") as f:
#     f.write(resp.get(srcUrl).content)


