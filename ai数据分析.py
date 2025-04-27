from pathlib import Path
from openai import OpenAI
import json
import time

client = OpenAI(
    api_key = "sk-3eCRX1ScglSPKk0pZw5lWX9qGtpmsxVcg5P0Iyl2d3dab8N3",
    base_url = "https://api.moonshot.cn/v1",
)
i=978
while i<1186:
    time.sleep(3)
    # xlnet.pdf 是一个示例文件, 我们支持 pdf, doc 以及图片等格式, 对于图片和 pdf 文件，提供 ocr 相关能力
    file_object = client.files.create(file=Path(f"article\{i}.json"), purpose="file-extract")
    
    # 获取结果
    # file_content = client.files.retrieve_content(file_id=file_object.id)
    # 注意，之前 retrieve_content api 在最新版本标记了 warning, 可以用下面这行代替
    # 如果是旧版本，可以用 retrieve_content
    file_content = client.files.content(file_id=file_object.id).text
    
    system_prompt = """
    每篇文章的分析结果以JSON格式输出，包含摘要、关键词、关键词逻辑关系和情感倾向。读取文章内容并按ID排序。对每篇文章进行文本摘要生成。提取关键词并分析其逻辑关系。进行情感分析，确定文章的情感倾向。请读取所有文章并输出
    请使用如下 JSON 格式输出你的回复：
    [ 
        {
            "id": 文章id,
            "summary": "文章总结",
            "keywords": [
                "关键词1（5个左右）",
                "关键词2",
                "关键词3",
                "关键词4",
                "关键词5",
            ],
            "keyword_relations": {
                "关键词a,关键词b": "关键词a与关键词b的逻辑联系"(尽量每个关键词都有),
            },
            "sentiment": "情感倾向"
        },
        .......(其他文章结构）
    ]
    """

    # 把它放进请求中
    messages = [
        {
        "role": "system",
        "content": "你是一位资深的文本分析专家，精通自然语言处理技术，能够快速提取文本的核心信息。同时，你也是数据处理工程师，擅长将复杂的数据结构化输出，确保信息的完整性和准确性。你具备强大的文本分析能力，包括文本摘要生成、关键词提取、情感分析以及逻辑关系识别。你还擅长使用JSON格式进行数据组织和输出，确保数据的可读性和可操作性。"
        },
        {   "role": "system", 
            "content": file_content
        }, # <-- 将附带输出格式的 system prompt 提交给 Kimi
        {   "role": "user", 
            "content":system_prompt
        }
    ]
    
    # 然后调用 chat-completion, 获取 Kimi 的回答
    completion = client.chat.completions.create(
    model="moonshot-v1-32k",
    messages=messages,
    temperature=0.3,
    response_format={"type": "json_object"},
    )

    content =completion.choices[0].message.content

    with open(f'res/res{i}.json','w',encoding='utf-8')as file:
        file.write(content)
    print(f"已经输出完毕{i}篇")
    i=i+1
print("已全部输出完毕")