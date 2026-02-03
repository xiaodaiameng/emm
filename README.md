crawlerintroduction

### requirements

bs4, playwright, requests, (os)

### customized paths

TARGET_URL，SAVE_DIR，EDGE_PATH（, COOKIE_PATH)

### 一、数据呈现情况

#### 1、在网页右键网页源代码里

直接response拿取整个html。

```
response = requests.get(url, headers=headers)
```

目标：html的内容

```
response.text
```

#### 2、在网页右键检查里的源代码

##### ①仅需Headers：

可以用response结合Headers，也可以用playwright+浏览器无头模式。

```
headers = {
    "User-Agent": "...",
    # "Referer": "...",
    "Cookie": "..."
}
```

##### ②非人机证明：

如滑块验证，或者纯需要个弹窗。

无需下载浏览器驱动，因为playwright 自带了！

```
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False, # 有头模式（显示浏览器窗口）
        slow_mo=300, # 操作延迟 300 毫秒
        args=["--disable-popup-blocking"] # 禁用弹窗拦截
    )
    page = browser.new_page()
    page.set_viewport_size({"width": 400, "height": 300})  # 设置窗口大小
    try:
        if os.path.exists(COOKIE_PATH):
            # 若 Cookie 文件存在，先加载网页再添加 Cookie 并刷新
            page.goto(TARGET_URL, wait_until="domcontentloaded")
            with open(COOKIE_PATH, 'r', encoding='utf-8') as f:
                cookies = eval(f.read())  # cookies 被转换成字符串（建议用 json 序列化）
                page.context.add_cookies(cookies)
            page.reload(wait_until="domcontentloaded")
            print("保存的Cookie有效，跳过验证")
        else:
            # 若 Cookie 文件不存在，先访问网页获取 Cookie 并保存
            page.goto(TARGET_URL, wait_until="domcontentloaded")
            cookies = page.context.cookies()
            with open(COOKIE_PATH, 'w', encoding='utf-8') as f:
                f.write(str(cookies))
            print("Cookie已保存")
        page.wait_for_load_state("networkidle")  # 等待网络空闲
        page_source = page.content()  # 获取网页 HTML 内容
        soup = BeautifulSoup(page_source, 'html.parser')  # 用 bs4解析
        # 提取数据...
    finally:
        browser.close() 
```

### 二、数据提取

#### 1、bs4

功能强大的HTML/XML 解析库，提取各种标签（\<p>, \<div>, \<src>.etc）

```
get
```

```
find
```

```
findall
```

```
find_parent
```

#### 2、re

#### 3、playwright

```
wait_for_selector
```

#### 4、requests

代码内部还有新的 url 要解析

#### 5、其他

数组方法；

滚动屏幕方法；

浏览器环境的原生方法：

```
document.querySelectorAll()
```

unquote：避免中文乱码

```
decoded_soup_name = unquote(encoded_soup_name, encoding='utf-8')
```

### 三、数据保存

#### 1、文本

```
with open(save_path, 'w', encoding='utf-8') as f:
						f.write(...)
```

#### 2、图片

```
with open(save_path, "wb") as f:
						f.write(...)
```

#### 3、视频

找到 .m3u8 or .mp4，下载即可。关键在找。
