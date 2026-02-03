import requests

#会话
session = requests.session()

data = {
    "loginName":"",
    "password":""
}

#登录
url = ""
session.post(url, data = data)

#拿书架上的数据
resp = session.get("https://user.17k.com/......", headers={ "Cookie":""})
print(resp.text)
print(resp.cookies)

