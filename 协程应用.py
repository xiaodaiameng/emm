import asyncio
import json

from fastapi import requests


async def download(url):
    print("假设现在开始下载。睡眠两秒演示。")
    await asyncio.sleep(2)
    print("下载完成")

asyncio def main():
    urls = [
        "",
        "",
        ""
    ]

    tasks = []
    for url in urls:
        d = download(url)

# 爬西游记：用同步操作访问 getCatalog，拿到所有章节的 cid和名称。用异步操作访问 gerChapterContent 下载文章内容

async def aiodownload(cid, b_id, title):
    data = {
        "book_id" : b_id,
        "cid" : f"{b_id} | {cid}",
        "need_bookinfo" : 1
    }
    data = json.dumps(data)
    url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={data}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url + data) as response:
            dic = await resp.json()
            async with aiofiles.open(title, mode="w", encoding="utf-8") as f:
                # f.write(dic['data']['novel']['content'])
async def getCatalog(url):
    resp = requests.get(url)
    dic = resp.json()
    tasks = []
    for item in dic["data"]['novel']['items']: # item对应每一个章节的名称和 cid
        title = item["title"]
        cid = item["cid"]

        # 准备异步任务
        tasks.append(aiodownload(cid, cid, title))
        print(cid, title)
    asyncio.run(asyncio.wait(tasks))
    await asyncio.wait(tasks)

if __name__ == '__main__':
    b_id = "4523456561"
    url = 'http://dushu.baidu.com/api/pc/getCatalog?data={  "book_id"  :  ' + b_id + '  }'
    asyncio.run(getCatalog(url))