from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 设置浏览器驱动
driver = webdriver.Edge()  # 使用Chrome浏览器驱动，确保已安装并配置好
key=["婚恋观念","婚姻成本","择偶标准","婚恋压力","社交媒体与婚恋","性别差异","婚恋心理","婚恋教育","婚恋市场","婚恋法律与政策","婚恋与职业发展","婚恋与生育","婚恋与文化","婚恋与心理健康","婚恋与经济状况","婚恋与年龄因素","婚恋与地区差异"]

# 创建一个txt文件来保存链接
with open("links.txt", "w", encoding="utf-8") as file:
    collections = set()
    for i in key:
        url = f"https://weixin.sogou.com/weixin?type=2&s_from=input&query={i}&ie=utf8&_sug_=y&_sug_type_=-1&w=01015002&oq=1234&ri=4&sourceid=sugg&stj=3%3B3%3B0%3B0&stj2=0&stj0=3&stj1=3&hp=111&hp1=&sut=2858&sst0=1742953181346&lkt=0%2C0%2C0"
        driver.get(url)
        # 循环收集链接并翻页
        while True:
            try:
                # 等待页面加载完成，找到所有符合条件的链接元素
                link_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3 a"))
                )

                # 收集链接
                for link in link_elements:
                    href = link.get_attribute("href")
                    if href and href.startswith("http"):
                        file.write(href + "\n")
                        print(f"已收集链接：{href}")

                # 尝试找到并点击下一页按钮
                next_page_button = driver.find_element(By.LINK_TEXT, "下一页")
                next_page_button.click()
                print("已翻页到下一页")
                time.sleep(2)  # 等待页面加载

            except Exception as e:
                print(f"翻页或收集链接时出错：{e}")
                break

# 关闭浏览器
driver.quit()
print("链接收集完成，已保存到 collected_links.txt 文件中")