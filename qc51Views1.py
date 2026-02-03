import json
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

TARGET_URL = "https://search.51job.com/list/000000,000000,0000,00,9,99,%E9%87%91%E8%9E%8D,2,1.html"
DATA_SAVE_PATH = os.path.join(r"D:\PythonCode\PyCrawler\small_project\Comments\JobWeb", "51job_recruits.json")
MY_WEBSITE_HTML = os.path.join(r"D:\PythonCode\PyCrawler\small_project\Comments\JobWeb", "recruit_website3.html")

def get_page_html():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, channel="chrome")
            page = browser.new_page()
            page.set_viewport_size({"width": 400, "height": 300})
            page.goto(TARGET_URL, wait_until="networkidle")
            page.wait_for_timeout(1000)
            page_html = page.content()
            browser.close()
            return page_html
    except Exception as e:
        print(f"获取页面失败：{str(e)}")
        return None
def parse_recruit_info(page_html):
    if not page_html:
        return []
    soup = BeautifulSoup(page_html, "lxml")
    recruit_list = []
    # 目标class为“joblist-item-job”
    job_items = soup.find_all("div", class_="joblist-item-job")
    if not job_items:
        print("未找到职位列表元素")
        return []
    for idx, job in enumerate(job_items, 1):
        try:
            sensors_data = job.get("sensorsdata")
            if sensors_data:
                # # 解析JSON格式的sensorsdata（注意转义字符（其实是复制粘贴的缺点））
                # sensor_json = json.loads(sensors_data.replace("&quot;", "\""))
                sensor_json = json.loads(sensors_data)
                job_id = sensor_json.get("jobId", "") 
                job_title = sensor_json.get("jobTitle", "")
                job_salary = sensor_json.get("jobSalary", "")
                job_area = sensor_json.get("jobArea", "")
                job_year = sensor_json.get("jobYear", "")
                job_degree = sensor_json.get("jobDegree", "")
            else:
                return "失败，网页源码已变更"
            company_name = job.find("a", class_="cname").get_text(strip=True) if job.find("a", class_="cname") else ""
            company_url = job.find("a", class_="cname")["href"] if (
                        job.find("a", class_="cname") and "href" in job.find("a", class_="cname").attrs) else ""
            company_industry = job.find_all("span", class_="dc")[0].get_text(strip=True) if len(
                job.find_all("span", class_="dc")) > 0 else ""
            company_type = job.find_all("span", class_="dc")[1].get_text(strip=True) if len(
                job.find_all("span", class_="dc")) > 1 else ""
            tags = [tag.get_text(strip=True)+"，" for tag in job.find_all("div", class_="tag")] if job.find("div",
                                                                                                           class_="tags") else []
            apply_url = job.find("button", class_="apply")["onclick"].split("'")[1] if (
                    job.find("button", class_="apply") and "onclick" in job.find("button",
                                                                                 class_="apply").attrs) else ""
            recruit_info = {
                "序号": idx,
                "职位ID": job_id,
                "职位名称": job_title,
                "薪资": job_salary,
                "工作地点": job_area,
                "工作年限": job_year,
                "学历要求": job_degree,
                "公司名称": company_name,
                "公司链接": company_url,
                "公司行业": company_industry,
                "公司性质": company_type,
                "岗位标签": tags,
                "投递链接": apply_url
            }
            recruit_list.append(recruit_info)
            print(f"提取第{idx}条职位：{job_title}")
        except Exception as e:
            print(f"提取第{idx}条职位失败：{str(e)}")
            continue
    return recruit_list

def save_recruit_data(recruit_list):
    if not recruit_list:
        print("无数据可保存")
        return
    try:
        with open(DATA_SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(recruit_list, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到：{DATA_SAVE_PATH}")
    except Exception as e:
        print(f"保存数据失败：{str(e)}")

def generate_website(recruit_list):
    if not recruit_list:
        print("无数据可生成网站")
        return
    html_content = f'''<!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                    <meta charset="UTF-8">
                    <title>招聘信息网站</title>
                </head>
                <body>
                    <div>
                        <h1>行业招聘信息</h1>
                        <p>共找到 {len(recruit_list)} 条有效职位，数据来源：前程无忧</p>
                    </div>
    '''
    for recruit in recruit_list:
        tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in recruit["岗位标签"]])
        card_html = f'''
        <div>
                <h3><a href="{recruit['投递链接']}">{recruit['职位名称']}</a></h3>
                <span>{recruit['薪资']}</span>
            </div>
            <div>
                    <span>公司：</span>
                    <span><a href="{recruit['公司链接']}">{recruit['公司名称']}</a></span>
                </div>
                <div>
                    <span>地点：</span>
                    <span class="info-value">{recruit['工作地点']}</span>
                </div>
                <div>
                    <span>年限：</span>
                    <span>{recruit['工作年限']}</span>
                </div>
                <div>
                    <span>学历</span>
                    <span>{recruit['学历要求']}</span>
                </div>
                <div>
                    <span>行业：</span>
                    <span>{recruit['公司行业']}</span>
                </div>
                <div>
                    <span>性质：</span>
                    <span>{recruit['公司性质']}</span>
                </div>
            </div>
            <div>
                岗位标签：{tags_html}
            </div>
        </div>
        '''
        html_content += card_html
        html_content += '''
                        </body>
                        </html>
                        '''
    try:
        with open(MY_WEBSITE_HTML, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"招聘网站已生成：{MY_WEBSITE_HTML}")
        print(f"用浏览器打开 {MY_WEBSITE_HTML} 即可查看")
    except Exception as e:
        print(f"生成网站失败：{str(e)}")

def main():
    page_html = get_page_html()
    if not page_html:
        return
    recruit_list = parse_recruit_info(page_html)
    if not recruit_list:
        return
    save_recruit_data(recruit_list)
    generate_website(recruit_list)
    print("抓取完成")

if __name__ == "__main__":
    main()