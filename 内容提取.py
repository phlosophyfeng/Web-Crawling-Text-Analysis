import requests
from bs4 import BeautifulSoup
import json
import re

urls = []
i = 0
articles = []  # 创建一个列表来存储所有文章数据

try:
    with open('url.txt', 'r', encoding='utf-8') as links:
        urls = [line.strip() for line in links]
except FileNotFoundError:
    print("文件 url.txt 未找到，请确保文件存在。")
    exit()

for url in urls:
    i += 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时出错：{e}")
        continue

    try:
        soup = BeautifulSoup(response.content, 'lxml')
        if soup.find(text=re.compile("该内容已被发布者删除")):
            print(f"Skipping URL {url} as the content has been deleted by the publisher.")
            continue
        else:
            title = soup.find('h1').get_text(strip=True)
            content = soup.find('div', class_='rich_media_content').get_text(strip=True)
            author = soup.find('a', class_='wx_tap_link js_wx_tap_highlight weui-wa-hotarea').get_text(strip=True)
            pattern = re.compile(r"var\s+createTime\s*=\s*'([^']+)';")
            a_time = soup.find(text=pattern)
            match = pattern.search(a_time)
            time = match.group(1) if match else None
            print(f"已读取到第{i}篇")
            article_data = {
                "id": i,
                "title": title,
                "content": content,
                "author": author,
                "time": time
            }
            articles.append(article_data)  # 将文章数据添加到列表中
    except AttributeError as e:
        print(f"解析 {url} 时出错：{e}")
        continue

try:
    with open('1.json', 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)
    print("数据已成功写入 1.json 文件。")
except Exception as e:
    print(f"写入 JSON 文件时出错：{e}")