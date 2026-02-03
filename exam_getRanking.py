import requests
import re
import os

# 目标URL和请求头（可根据实际需求修改headers）
TARGET_URL = "https://www.bankhr.com/so/top10/all/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "Referer": "https://www.bankhr.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

# HTML输出路径（按你的要求设置为 small_project/Comments/Ranking/ranking.html）
HTML_OUTPUT_PATH = os.path.join("../Comments", "Ranking", "ranking.html")


def crawl_ranking_data():
    """爬取金融英才网全国职位排行榜原始数据"""
    try:
        # 发送请求获取页面内容
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        response.encoding = "utf-8"  # 强制指定编码，避免中文乱码
        response.raise_for_status()  # 状态码非200时抛出异常

        # 正则匹配页面中JavaScript的职位数据数组（核心提取逻辑）
        data_pattern = re.compile(
            r"array\(\d+\) \{\s*((?:\[\d+\]=>\s*array\(11\) \{(?:.|\s)*?\}\s*)*)\}",
            re.MULTILINE
        )
        item_pattern = re.compile(r"\[\d+\]=>\s*array\(11\) \{\s*(.*?)\s*\}", re.DOTALL)
        key_value_pattern = re.compile(r'\["(\w+)"\]=>\s*string\(\d+\) "([^"]*)"')

        # 提取外层数据结构
        data_match = data_pattern.search(response.text)
        if not data_match:
            print("❌ 未从页面中找到职位排行榜数据")
            return None

        # 解析每个职位的详细信息
        ranking_data = []
        items = item_pattern.findall(data_match.group(1))
        for item in items:
            job_info = {}
            # 提取键值对（如 job_id、job_name、pub_nums 等）
            key_values = key_value_pattern.findall(item)
            for key, value in key_values:
                job_info[key] = value
            # 过滤有效数据（确保包含核心字段）
            if all(k in job_info for k in ["job_id", "job_name", "pub_nums", "salary"]):
                ranking_data.append(job_info)

        print(f"✅ 成功爬取 {len(ranking_data)} 条原始职位数据")
        return ranking_data

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败：{str(e)}")
        return None
    except Exception as e:
        print(f"❌ 数据解析失败：{str(e)}")
        return None


def process_raw_data(raw_data):
    """处理原始数据，格式化薪资、计算进度条百分比"""
    if not raw_data:
        return []

    # 1. 薪资格式化函数（统一展示格式）
    def format_salary(salary_str):
        try:
            salary = int(salary_str)
            if salary >= 1000000:
                return "面议"
            elif salary >= 10000:
                return f"{salary // 1000}k/月"
            else:
                return f"{salary}元/月"
        except (ValueError, TypeError):
            return "面议"

    # 2. 计算进度条百分比（以最大发布量为100%基准）
    pub_nums_list = [int(item["pub_nums"]) for item in raw_data if item["pub_nums"].isdigit()]
    max_pub_num = max(pub_nums_list) if pub_nums_list else 100  # 避免除以0

    # 3. 整理每条数据的最终格式
    processed_list = []
    for item in raw_data:
        pub_num = int(item["pub_nums"]) if item["pub_nums"].isdigit() else 0
        processed_list.append({
            "rank": len(processed_list) + 1,  # 排名（从1开始）
            "job_name": item["job_name"],
            "job_url": f"https://www.bankhr.com/so/{item['job_id']}.html",  # 职位详情链接
            "pub_nums": pub_num,  # 发布数量
            "pub_percent": min(int((pub_num / max_pub_num) * 100), 100),  # 进度条百分比（最大100%）
            "salary": format_salary(item["salary"]),  # 格式化后薪资
            "city": item.get("city_name", "全国")  # 地区（默认全国）
        })

    # 按发布数量降序排序（确保排名准确）
    return sorted(processed_list, key=lambda x: x["pub_nums"], reverse=True)


def generate_ranking_html(processed_data):
    """生成排行榜HTML内容（仅含排行榜，无多余文字）"""
    # 处理无数据场景
    if not processed_data:
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>排行榜</title>
            <style>
                body { font-family: "Microsoft YaHei", sans-serif; max-width: 1200px; margin: 0 auto; padding: 40px 20px; background: #f5f7fa; }
                .empty-tip { text-align: center; padding: 80px 0; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
                .empty-tip p { font-size: 18px; color: #7f8c8d; margin: 0; }
            </style>
        </head>
        <body>
            <div class="empty-tip">
                <p>暂无职位排行榜数据</p>
            </div>
        </body>
        </html>
        """

    # 生成职位列表HTML片段
    job_items_html = ""
    for item in processed_data:
        # 前三名排名数字特殊颜色（1:红、2:橙、3:绿）
        rank_color = "#e74c3c" if item["rank"] == 1 else "#f39c12" if item["rank"] == 2 else "#2ecc71"
        job_items_html += f"""
        <li class="ranking-item">
            <div class="rank-num" style="background: {rank_color};">{item['rank']}</div>
            <div class="job-info">
                <a href="{item['job_url']}" target="_blank" class="job-name">{item['job_name']}</a>
                <div class="job-meta">地区：{item['city']} | 薪资：{item['salary']}</div>
            </div>
            <div class="progress-box">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {item['pub_percent']}%"></div>
                </div>
            </div>
            <div class="pub-count">{item['pub_nums']}个</div>
        </li>
        """

    # 完整HTML模板（仅含排行榜相关内容）
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>排行榜</title>
        <style>
            /* 基础样式重置 */
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: "Microsoft YaHei", Arial, sans-serif; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 30px 20px; 
                background-color: #f5f7fa; 
            }}

            /* 排行榜标题 */
            .ranking-title {{ 
                text-align: center; 
                font-size: 28px; 
                font-weight: 600; 
                color: #2c3e50; 
                margin: 0 0 30px; 
            }}

            /* 职位列表容器 */
            .ranking-list {{ 
                list-style: none; 
                padding: 0; 
            }}

            /* 单个职位项样式 */
            .ranking-item {{ 
                display: flex; 
                align-items: center; 
                padding: 16px 20px; 
                margin-bottom: 12px; 
                background: white; 
                border-radius: 10px; 
                box-shadow: 0 2px 6px rgba(0,0,0,0.05); 
                transition: box-shadow 0.3s ease; 
            }}
            .ranking-item:hover {{ 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
            }}

            /* 排名数字 */
            .rank-num {{ 
                width: 42px; 
                height: 42px; 
                line-height: 42px; 
                text-align: center; 
                color: white; 
                border-radius: 50%; 
                margin-right: 20px; 
                font-weight: bold; 
                font-size: 16px; 
            }}

            /* 职位信息区域 */
            .job-info {{ 
                flex: 1; /* 占满剩余宽度 */
            }}
            .job-name {{ 
                font-size: 18px; 
                font-weight: 600; 
                color: #2c3e50; 
                text-decoration: none; 
                margin-bottom: 6px; 
                display: inline-block; 
            }}
            .job-name:hover {{ 
                color: #3498db; 
                text-decoration: underline; 
            }}
            .job-meta {{ 
                font-size: 14px; 
                color: #7f8c8d; 
            }}

            /* 进度条容器 */
            .progress-box {{ 
                width: 400px; 
                margin: 0 30px; 
            }}
            .progress-bar {{ 
                height: 12px; 
                background: #e0e6ed; 
                border-radius: 6px; 
                overflow: hidden; 
            }}
            .progress-fill {{ 
                height: 100%; 
                background: #2ecc71; 
                border-radius: 6px; 
                transition: width 0.5s ease; 
            }}

            /* 发布数量统计 */
            .pub-count {{ 
                width: 100px; 
                text-align: center; 
                font-size: 14px; 
                color: #2c3e50; 
                font-weight: 500; 
            }}

            /* 响应式适配（手机/平板） */
            @media (max-width: 992px) {{
                .progress-box {{ width: 300px; margin: 0 20px; }}
            }}
            @media (max-width: 768px) {{
                .ranking-item {{ flex-direction: column; align-items: flex-start; }}
                .progress-box {{ width: 100%; margin: 12px 0; }}
                .pub-count {{ width: auto; margin-top: 10px; }}
                .ranking-title {{ font-size: 24px; }}
            }}
        </style>
    </head>
    <body>
        <h1 class="ranking-title">排行榜</h1>
        <ul class="ranking-list">
            {job_items_html}
        </ul>
    </body>
    </html>
    """
    return full_html


def save_html_to_file(html_content):
    """保存HTML内容到指定路径（自动创建不存在的文件夹）"""
    try:
        # 确保输出文件夹存在（不存在则创建）
        output_dir = os.path.dirname(HTML_OUTPUT_PATH)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"✅ 已创建文件夹：{output_dir}")

        # 写入HTML文件
        with open(HTML_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ HTML文件已生成：{os.path.abspath(HTML_OUTPUT_PATH)}")

    except Exception as e:
        print(f"❌ 保存HTML文件失败：{str(e)}")


if __name__ == "__main__":
    print("=" * 50)
    print("开始执行金融英才网职位排行榜爬取任务")
    print("=" * 50)

    # 1. 爬取原始数据
    raw_data = crawl_ranking_data()
    if not raw_data:
        # 无数据时生成空页面
        save_html_to_file(generate_ranking_html([]))
        print("任务结束（无有效数据）")
        exit()

    # 2. 处理原始数据
    processed_data = process_raw_data(raw_data)
    print(f"✅ 成功处理 {len(processed_data)} 条职位数据")

    # 3. 生成并保存HTML
    html_content = generate_ranking_html(processed_data)
    save_html_to_file(html_content)

    print("=" * 50)
    print("任务执行完成！")
    print("=" * 50)