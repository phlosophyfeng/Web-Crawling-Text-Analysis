from openai import OpenAI
from pathlib import Path
import json

client = OpenAI(
    api_key = "sk-T3vYc2BosbTPM0b1AP4ERrENatYnIGI0TiH8YSFRbUbWGAso",
    base_url="https://api.moonshot.cn/v1/",
)
file_list = client.files.list()
 
for file in file_list.data:
    client.files.delete(file.id)
    print("已删除")
 
print("清理完毕")