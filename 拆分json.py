import json
import os

def split_json(input_file, output_dir, chunk_size=1000):
    """
    将一个大的 JSON 文件拆分成多个小的 JSON 文件。
    
    参数:
        input_file (str): 输入的 JSON 文件路径
        output_dir (str): 输出文件夹路径
        chunk_size (int): 每个输出文件包含的条目数量，默认为 1000
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 检查数据是否是列表
    if not isinstance(data, list):
        raise ValueError("输入的 JSON 数据不是列表格式，无法拆分。")
    
    # 拆分数据
    total_chunks = (len(data) + chunk_size - 1) // chunk_size  # 计算总块数
    for i in range(total_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk_data = data[start:end]
        
        # 生成输出文件名
        output_file = os.path.join(output_dir, f"{i+1}.json")
        
        # 写入拆分后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, ensure_ascii=False, indent=4)
        
        print(f"已生成文件: {output_file}, 包含 {len(chunk_data)} 条记录")

if __name__ == "__main__":
    # 示例使用
    input_file = "1.json"  # 输入的 JSON 文件
    output_dir = "article"     # 输出文件夹
    chunk_size = 1               # 每个文件的条目数量
    
    split_json(input_file, output_dir, chunk_size)
    print("拆分完成！")