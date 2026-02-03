
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# 初始化Edge浏览器
def test_edge_browser():
    # 配置Edge驱动路径（根据实际情况修改）
    edge_driver_path = "msedgedriver.exe"  # 如果已加入环境变量可直接写文件名

    try:
        # 初始化驱动服务
        service = Service(edge_driver_path)

        # 启动Edge浏览器
        driver = webdriver.Edge(service=service)

        # 打开测试网页（使用百度首页作为示例）
        driver.get("https://www.baidu.com")
        print("成功打开百度首页")

        # 等待页面加载完成，最多等待10秒
        wait = WebDriverWait(driver, 10)

        # 查找搜索框并输入内容
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        search_box.send_keys("Selenium Edge测试")
        print("已在搜索框输入内容")

        # 查找搜索按钮并点击
        search_button = wait.until(
            EC.element_to_be_clickable((By.ID, "su"))
        )
        search_button.click()
        print("已点击搜索按钮")

        # 等待搜索结果加载
        time.sleep(3)

        # 获取搜索结果标题
        results = driver.find_elements(By.CSS_SELECTOR, "h3.t a")
        print(f"\n找到{len(results)}个搜索结果：")
        for i, result in enumerate(results[:5], 1):  # 只显示前5个结果
            print(f"{i}. {result.text}")

    except Exception as e:
        print(f"测试过程中出错：{str(e)}")

    finally:
        # 等待几秒后关闭浏览器
        time.sleep(5)
        driver.quit()
        print("\n浏览器已关闭")


if __name__ == "__main__":
    test_edge_browser()

# 刚出生的失败案例笔记聚合地
#         if i % 5 == 0:
#             time.sleep(random.uniform(2, 4))
#     # 4. 保存结果
#     with open('Comments/MusicComments/high_like_comments.json', 'w', encoding='utf-8') as f:
#         json.dump(all_comments, f, ensure_ascii=False, indent=2)
#     print(f"\n爬取完成，共获取 {len(all_comments)} 条符合要求的评论，已保存到 high_like_comments.json")

# if __name__ == '__main__':
#     main()
