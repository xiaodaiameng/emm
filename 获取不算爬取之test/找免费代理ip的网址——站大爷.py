# 改代理的操作：
proxies = {
    "http": "http://127.0.0.1:1080",
}
resp = requests.get("url", proxies=proxies)
# 其他一致