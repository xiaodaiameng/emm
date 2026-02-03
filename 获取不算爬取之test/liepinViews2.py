import json
import os
import re
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# ---------------------- 1. 配置参数 ----------------------
TARGET_URL = "https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage=0&pageSize=40&key=%E9%87%91%E8%9E%8D&suggestTag=&workYearCode=1&compId=&compName=&compTag=&industry=&salaryCode=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&otherCity=&sfrom=search_job_pc"
JOB_WEB_DIR = r"D:\PythonCode\PyCrawler\small_project\Comments\JobWeb"
os.makedirs(JOB_WEB_DIR, exist_ok=True)
DATA_SAVE_PATH = os.path.join(JOB_WEB_DIR, "liepin_recruits.json")
MY_WEBSITE_HTML = os.path.join(JOB_WEB_DIR, "liepin_my_website.html")
PAGE_RANGE = range(0, 1)  # 抓取第1页


# ---------------------- 2. 获取页面HTML ----------------------
def get_page_html():
    page_html_list = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                channel="chrome",
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            page = browser.new_page()

            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/123.0.0.0 Safari/537.36"
            ]
            page.set_extra_http_headers({"User-Agent": random.choice(user_agents)})

            for page_num in PAGE_RANGE:
                current_url = re.sub(r"currentPage=\d+", f"currentPage={page_num}", TARGET_URL)
                print(f"🔍 抓取第{page_num + 1}页：{current_url}")

                page.goto(current_url, wait_until="networkidle")
                page.wait_for_selector('a[data-nick="job-detail-job-info"]', timeout=10000)
                page.wait_for_timeout(random.randint(1000, 2000))

                page_html = page.content()
                page_html_list.append(page_html)
                print(f"✅ 第{page_num + 1}页HTML抓取完成")

            browser.close()
            return page_html_list
    except Exception as e:
        print(f"❌ 抓取页面失败：{str(e)}")
        return []


# ---------------------- 3. 核心修复：解析函数（确保strip()是字符串方法） ----------------------
def parse_job_info(page_html_list):
    all_jobs = []
    if not page_html_list:
        return all_jobs

    for page_idx, page_html in enumerate(page_html_list, 1):
        soup = BeautifulSoup(page_html, "lxml")
        job_links = soup.find_all('a', attrs={"data-nick": "job-detail-job-info"})

        if not job_links:
            print(f"❌ 第{page_idx}页未找到目标职位标签")
            continue

        for job_idx, job_link in enumerate(job_links, 1):
            try:
                # 1. 职位详情链接（修复：确保href是字符串后调用strip()）
                job_href = job_link.get("href", "").strip()  # 正确：字符串对象.strip()
                job_url = f"https://www.liepin.com{job_href}" if job_href.startswith("/") else job_href

                # 2. 职位名称（修复：先判断元素存在，再对文本调用strip()）
                job_title = "未知职位"
                job_title_elem = job_link.find("div", class_=re.compile(r"ellipsis-1"))
                if job_title_elem:
                    job_title = job_title_elem.get_text().strip()  # 正确：文本字符串.strip()

                # 3. 薪资（修复：同上，先判断元素，再处理文本）
                salary = "薪资面议"
                salary_elem = job_link.find("span", class_=re.compile(r"job-salary"))
                if salary_elem:
                    salary = salary_elem.get_text().strip()  # 正确：文本字符串.strip()

                # 4. 工作地点（修复：对标签文本调用strip()）
                location = "未知地点"
                location_box = job_link.find("div", class_=re.compile(r"job-dq-box"))
                if location_box:
                    location_text = location_box.get_text().strip()  # 正确：文本字符串.strip()
                    location_match = re.search(r"【([^】]+)】", location_text)
                    if location_match:
                        location = location_match.group(1).strip()  # 正确：匹配结果字符串.strip()

                # 5. 岗位标签（修复：对每个标签文本调用strip()）
                job_labels = []
                label_elems = job_link.find_all("span", class_=re.compile(r"labels-tag"))
                for label in label_elems:
                    label_text = label.get_text().strip()  # 正确：文本字符串.strip()
                    if label_text:  # 过滤空标签
                        job_labels.append(label_text)

                # 6. 职位标签（修复：处理文本）
                urgent_tag = "普通职位"
                urgent_tag_elem = job_link.find("span", class_=re.compile(r"job-tag"))
                if urgent_tag_elem:
                    urgent_tag = urgent_tag_elem.get_text().strip()  # 正确：文本字符串.strip()

                # 7. 职位ID（修复：对链接文本处理）
                job_id = f"page{page_idx}_job{job_idx}"
                job_id_match = re.search(r"(\d+)\?", job_href)
                if job_id_match:
                    job_id = job_id_match.group(1).strip()  # 正确：匹配结果字符串.strip()

                # 整理数据
                job_info = {
                    "序号": len(all_jobs) + 1,
                    "页码": page_idx,
                    "职位ID": job_id,
                    "职位名称": job_title,
                    "薪资": salary,
                    "工作地点": location,
                    "岗位标签": job_labels,
                    "职位标签": urgent_tag,
                    "详情链接": job_url
                }
                all_jobs.append(job_info)
                print(f"✅ 第{page_idx}页第{job_idx}条：{job_title}（{salary} | {location}）")

            except Exception as e:
                print(f"❌ 解析第{page_idx}页第{job_idx}条失败：{str(e)}")
                continue

    return all_jobs


# ---------------------- 4. 保存数据 ----------------------
def save_data(jobs):
    if not jobs:
        print("❌ 无数据可保存")
        return
    try:
        with open(DATA_SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print(f"✅ 数据已保存到：{DATA_SAVE_PATH}（共{len(jobs)}条）")
    except Exception as e:
        print(f"❌ 保存数据失败：{str(e)}")


# ---------------------- 5. 生成展示网站 ----------------------
def generate_website(jobs):
    if not jobs:
        print("❌ 无数据生成网站")
        return
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>猎聘金融行业职位展示</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: "Microsoft YaHei", sans-serif; }}
        body {{ background: #f5f7fa; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin: 30px 0; padding-bottom: 20px; border-bottom: 1px solid #eee; }}
        .header h1 {{ color: #2c3e50; font-size: 28px; }}
        .header p {{ color: #7f8c8d; font-size: 16px; margin-top: 10px; }}
        .job-card {{ background: #fff; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: transform 0.3s; }}
        .job-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .card-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .job-title {{ font-size: 20px; color: #e74c3c; font-weight: bold; }}
        .job-salary {{ font-size: 18px; color: #27ae60; font-weight: bold; }}
        .card-mid {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px; }}
        .info-item {{ display: flex; align-items: center; }}
        .info-label {{ color: #7f8c8d; font-size: 14px; width: 80px; }}
        .info-value {{ color: #2c3e50; font-size: 14px; }}
        .tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }}
        .tag {{ padding: 4px 12px; border-radius: 20px; font-size: 13px; }}
        .label-tag {{ background: #e8f5e9; color: #2e7d32; }}
        .urgent-tag {{ background: #ffebee; color: #c62828; }}
        .detail-btn {{ display: inline-block; background: #3498db; color: #fff; padding: 8px 20px; border-radius: 5px; text-decoration: none; font-size: 14px; transition: background 0.3s; }}
        .detail-btn:hover {{ background: #2980b9; }}
        @media (max-width: 768px) {{
            .card-top {{ flex-direction: column; align-items: flex-start; gap: 10px; }}
            .info-item {{ width: 100%; margin-bottom: 5px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>猎聘网 - 金融行业应届生职位</h1>
            <p>共收录 {len(jobs)} 条有效职位（上海地区）</p>
        </div>
'''
    for job in jobs:
        labels_html = "".join([f'<span class="tag label-tag">{tag}</span>' for tag in job["岗位标签"]])
        card_html = f'''
        <div class="job-card">
            <div class="card-top">
                <div class="job-title">{job['职位名称']}</div>
                <div class="job-salary">{job['薪资']}</div>
            </div>
            <div class="card-mid">
                <div class="info-item">
                    <span class="info-label">地点：</span>
                    <span class="info-value">{job['工作地点']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">标签：</span>
                    <span class="info-value">{job['职位标签']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">职位ID：</span>
                    <span class="info-value">{job['职位ID']}</span>
                </div>
            </div>
            <div class="tags">
                {labels_html}
                <span class="tag urgent-tag">{job['职位标签']}</span>
            </div>
            <a href="{job['详情链接']}" target="_blank" class="detail-btn">查看职位详情</a>
        </div>
'''
        html_content += card_html
    html_content += '''
    </div>
</body>
</html>'''
    try:
        with open(MY_WEBSITE_HTML, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ 展示网站已生成：{MY_WEBSITE_HTML}")
    except Exception as e:
        print(f"❌ 生成网站失败：{str(e)}")


# ---------------------- 6. 主函数 ----------------------
def main():
    print("===== 开始抓取猎聘网目标职位信息 =====")
    page_htmls = get_page_html()
    if not page_htmls:
        print("❌ 未获取到页面数据")
        return
    job_list = parse_job_info(page_htmls)
    if not job_list:
        print("❌ 未解析到职位信息")
        return
    save_data(job_list)
    generate_website(job_list)
    print("===== 抓取流程完成 =====")


if __name__ == "__main__":
    main()