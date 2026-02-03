
import requests
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

# 找Call Stack 里的 data变动处
# 找 local里的 elx里的 request里的 url 和找 data加密的对应字母查找，data被变了的地方，那种字典->重要
# 找到未加密的参数
# window.arsea(参数，xxxx,xxx,xxx)
# 想办法把参数进行加密(必须参考网易的逻辑)，params.=>encText,encSecKey => encSecKey
# 拿到评论


url = "https://music.163.com"
拿首页的八宫格地址
data = {

    那种加密字典复制过来，重要
}
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# }
# response = requests.get(url, headers=headers)
#
# # 检查请求是否成功
# if response.status_code == 200:
#     # 设置正确的编码，防止中文乱码（网易云音乐网页一般是utf-8编码）
#     response.encoding = 'utf-8'
#     # 使用BeautifulSoup解析HTML内容
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # 使用CSS选择器查找所有符合条件的a标签（这里假设是你提供的那种结构的a标签）
#     a_tags = soup.select('a.msk[data-res-type="13"]')
#
#     for a_tag in a_tags:
#         # 获取href属性的值，即子页面的相对地址
#         relative_url = a_tag.get('href')
#         if relative_url:
#             # 拼接完整的URL
#             full_url = "https://music.163.com" + relative_url
#             print(full_url)
# else:
#     print(f"请求失败，状态码: {response.status_code}")

请求方式是post
data = {
    csrf_token:,
corsor:,
offset:,
orderType:,
pageNo:,
pageSize:,
rid:,
threadId:,
}

def get_encSecKey():
    return......
def get_params(data):
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second
def to_16(data):
    pad = 16 - len(data)%16
    data += chr(pad) * pad
    return data
def enc_params(data, key): # 加密过程
    iv =
    aes = AES.new(key=key.encode("utf-8"), IV = iv.encode("utf-8"), mode=AES.MODE_CBC)
    bs =
    return str(b64encode(bs), "utf-8")

requests.post(url, data={
    "params": get_params(json.dumps(data)),# 用 json把 data字典转为字符串
    "encSecKey": get_encSecKey(),回到 Network，找 encSecKey, 还有 Sources里找 encSecKey
})


