import requests
import re

# Introduction
sentence = "我的电话号码是：10086。小猪佩奇的电话号码是：10000pig。"
results = re.finditer(r'\d+', sentence)  # 生成迭代器
for match in results:
    print(match.group())  # 对每个匹配对象，调用group()获取匹配的字符串

# Before: get url:
# url = "https://movie.douban.com/top250"
# # 将 url里的参数重新封装
# param = {
#     "start": 0,
#     "filter": ""
# }
# headers={
#     "User-Agent":
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
# }
# response = requests.get(url, params=param, headers=headers)
# # print(response.request.headers) #打印请求头
# # print(response.request.url) # 打印网址
# response.close()

# TWO
domain = "网址"
resp = requests.get(domain, varify=False)
resp.encoding = 'utf-8'
html = resp.text # 可以写成：html = etree.HTML(resp.text)
print(html)

obj1 = re.compile(r"热片.*?<ul>(.*?)</ul>", re.S)# re.S 让 . 可以匹配换行符

result1 = obj1.finditer(html)
for match in result1:
    ul = match.group('ul')
    print(ul)# 在 ul里有子页面链接，使用新的匹配规则 obj2=...和 result2=... 提取，不作示例