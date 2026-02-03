import requests
import re
import hashlib
import time
import json


def get_baidu_token():
    """从百度翻译主页提取 token（适配最新页面结构）"""
    url = "https://fanyi.baidu.com/mtpe-individual/transText"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
    }

    # 发送请求获取页面 HTML
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ 获取页面失败，状态码：{response.status_code}")
        return None

    # 尝试多种可能的 token 格式（百度可能动态调整）
    html = response.text
    # 模式1：匹配 "token": "xxx"（双引号）
    token_match = re.search(r'"token"\s*:\s*"([^"]+)"', html)
    if not token_match:
        # 模式2：匹配 'token': 'xxx'（单引号）
        token_match = re.search(r'token\s*:\s*\'([^\']+)\'', html)
    if not token_match:
        # 模式3：匹配 window.token = "xxx"
        token_match = re.search(r'window\.token\s*=\s*"([^"]+)"', html)
    if not token_match:
        # 模式4：匹配 window.common.token = "xxx"
        token_match = re.search(r'window\.common\.token\s*=\s*"([^"]+)"', html)

    if token_match:
        return token_match.group(1)
    else:
        # 调试：打印部分 HTML 帮助分析（可选）
        print("⚠️ 未找到 token，页面可能更新。部分 HTML 内容：")
        print(html[:2000])  # 打印前2000字符
        return None


def generate_baidu_sign(query):
    """生成 sign 和 salt（时间戳）"""
    sign_key = "fanyideskweb"
    key = "Ygy_4c=r#e#4EX^NUGUc5"
    salt = str(int(time.time() * 1000))
    sign_str = f"{sign_key}{query}{salt}{key}".encode("utf-8")
    return hashlib.md5(sign_str).hexdigest(), salt


# 主逻辑
query = input("请输入要翻译的内容：")
token = get_baidu_token()

if token:
    sign, salt = generate_baidu_sign(query)
    url = "https://fanyi.baidu.com/v2transapi"
    data = {
        "from": "auto",
        "to": "en",
        "query": query,
        "transtype": "realtime",
        "simple_means_flag": "3",
        "sign": sign,
        "salt": salt,
        "token": token,
        "domain": "common"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://fanyi.baidu.com/mtpe-individual/transText",
        "Cookie": "BAIDUID_BFESS=F68700188F9EC55E75D217FF200584D5:FG=1; ZFY=7F0Och0p:AqeLrrgE6iijW0bJznTxRTkqRyvLKAtb7kc:C; BDUSS=dUd1Ria244R3hXSWpudjJFellhZzNOZ3dYZm44S0pZUHVKOXdjbFd1Y3pCcnRvSVFBQUFBJCQAAAAAAQAAAAEAAADpjNlhy7y~vLXE1e3NtwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADN5k2gzeZNoNE; BDUSS_BFESS=dUd1Ria244R3hXSWpudjJFellhZzNOZ3dYZm44S0pZUHVKOXdjbFd1Y3pCcnRvSVFBQUFBJCQAAAAAAQAAAAEAAADpjNlhy7y~vLXE1e3NtwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADN5k2gzeZNoNE; AIT_PERSONAL_VERSION=1; AIT_ENTERPRISE_VERSION=1; ab_sr=1.0.1_ODE2MjUyOTRjM2IyOWNiODY1ZTcxOGUzZWNlYmZmYjExNGIzMDc2M2QxZjM0Y2EwZWZhMTdlZTA5MWNjNjBiOGRkNGFmNDc2OTg0NDMxZWJjZDE2YzY4MWY5ZmExZTAzYzFhMGFkMWViYjI4MTVmNmMyY2JkZjBhNmZhOTNhMjE4Y2JmOTM1ODQxNTRiNmM2MDFiNzJiYTUzZDA3MWFkYjQwNTY2ODMxZTNjNjAwYmUxMTE1NDI0M2ViOGZmYzQyMDhmYmM3ZDYxZGNmNmJiY2JlNWU2M2IyNjM3MmRlZWQ=; RT=\"z=1&dm=baidu.com&si=700eb59d-474b-40f9-b9c2-853acf6b91ca&ss=meuwszv5&sl=5&tt=eh9&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1dtec&ul=1e2kc\""
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("\n翻译结果：")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            # 提取核心翻译文本
            if "trans_result" in result and result["trans_result"].get("data"):
                print("\n简洁结果：", result["trans_result"]["data"][0]["dst"])
        else:
            print(f"请求失败，状态码：{response.status_code}，内容：{response.text}")
    except Exception as e:
        print(f"错误：{e}")
else:
    print("❌ 未获取到 token，无法继续翻译。")

# query=input("输入你要搜索的内容，如明星：")# query = question + inquiry
# url = f"https://cn.bing.com/search?q={query}"
#
# dict = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
# }
# response = requests.get(url, headers=dict)
# print(response)
# print(response.text) # 打印出网页 html代码

response.close()