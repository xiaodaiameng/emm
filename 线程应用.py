import requests
from lxml import etree
import csv



# 先写出一张表：
#
# 老规矩，记得排除索引


f = open("data.csv", mode="w")
csvwriter = csv.writer(f)



def download_one_page(url):
    # 取页面源代码
    resp = requests.get(url)
    html = etree.HTML(resp.text)
    table = html.xpath("/html/body/div[2]/div[4]/div[1]/table")[0]
    trs = table.xpath("./tr")[1:]# 新发地菜价第一张表有21列，爬，拿到21个点
    # 也可以用其他写法爬：
    # trs = table.xpath("./tr[position()>1]")
    # 拿到每个tr
    for tr in trs:
        txt = tr.xpath("./td/text()")
        #简单处理一下再去打印
        txt = (item.replace("\\", "").replace("/", "") for item in txt)
        # print(txt)
        print(list(txt))
        # csvwriter.writerow(txt)
    print(len(trs))
    print(url, "提取完毕！")



# 多线程很多页表同时下载：


from concurrent.futures import ThreadPoolExecutor

if __name__ == '__main__':
    with ThreadPoolExecutor(50) as t:
        for i in range(1,100):
            t.submit(download_one_page, f"新发地网址列表/list/{i}.shtml")
    print("全部提取完毕！")


























