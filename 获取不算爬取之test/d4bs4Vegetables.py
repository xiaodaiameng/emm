import csv

import requests
from bs4 import BeautifulSoup

url = "菜价  网址"
response = requests.get(url)

f = open("菜价.csv", mode="wb")
csvWriter = csv.writer(f) # 写入之前先创建的写字对象

# 把页面源代码交给BeautifulSoup进行处理，生成bs对象
page = BeautifulSoup(response.text, "html.parser")

# 从bs对象中查找数据：如 find(标签，属性=值)，find_all(标签，属性=值)
dataname = page.find("table", attrs={"class": "hq_table"})# "table" 表示要查找的 HTML 标签类型是 <table>（表格标签）。
# attrs={"class": "hq_table"} 要求找到的 <table> 标签必须包含 class 属性，且该属性的值为 "hq_table"。

# 拿到所有数据行
trs = dataname.find_all("tr")[1:]
for tr in trs:
    tds = tr.find_all("td") # 拿到每行里的所有 td
    name = tds[0].text
    avg = tds[1].text # 拿到被标签标记的内容，以此类推
    kind = tds[2].text
    print(name, avg, kind)
    csvWriter.writerow([name, avg, kind])

f.close()
print("over——————————————————")

