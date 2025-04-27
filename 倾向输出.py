import json
import os

# 初始化情感统计字典
sentiment_count = {}

# 指定包含JSON文件的文件夹路径
folder_path = "res"  # 替换为你的文件夹路径

# 遍历文件夹中的所有JSON文件
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        
        # 读取JSON文件
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            # 获取情感倾向
            sentiment = data.get("sentiment", "未知")
            
            # 更新情感统计
            sentiment_count[sentiment] = sentiment_count.get(sentiment, 0) + 1

# 输出统计结果
print("情感倾向统计结果:")
for sentiment, count in sentiment_count.items():
    print(f"{sentiment}: {count} 次")
