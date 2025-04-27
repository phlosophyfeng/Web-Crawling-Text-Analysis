import json
import networkx as nx 
from pyvis.network import Network 

G = nx.DiGraph()
i = 0

while i < 500:
    i += 1
    file_path = f'res/res{i}.json'
    
    try:
        # 尝试打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        keywords = data['keywords']
        relations = data['keyword_relations']
        
        # 添加节点
        for keyword in keywords:
            G.add_node(keyword, title=keyword, label=keyword)
        
        # 添加边
        for relation, description in relations.items():
            try:
                source, target = relation.split(',')
                G.add_edge(source.strip(), target.strip(), title=description, weight=2)
            except ValueError as e:
                print(f"文件 {file_path} 中的关系解析错误: {e}")
                print(f"问题关系: {relation}")
    
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在，跳过处理")
    except json.JSONDecodeError as e:
        print(f"文件 {file_path} 的 JSON 格式错误: {e}")
    except KeyError as e:
        print(f"文件 {file_path} 缺少必要字段: {e}")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生未知错误: {e}")

# 使用 pyvis 进行可视化
net = Network(notebook=True, directed=True, height="1000px", width="100%")
net.from_nx(G)

# 调整布局和样式
net.repulsion(
    node_distance=300,
    central_gravity=0.01,
    spring_length=400,
    spring_strength=0.05,
    damping=0.1
)
net.toggle_physics(True)
net.barnes_hut()
# 显示交互式网络图
net.show("keyword_relationships.html")

# 假设 G 是已经构建好的图
# 这里直接使用之前的 G 对象

# 分析图的结构
analysis_results = {
    "nodes_count": G.number_of_nodes(),  # 节点数量
    "edges_count": G.number_of_edges(),  # 边数量
    "density": nx.density(G),  # 图的密度
    "connected_components": [list(component) for component in nx.weakly_connected_components(G)],  # 弱连通分量，将 set 转换为 list
    "degree_centrality": nx.degree_centrality(G),  # 度中心性
    "closeness_centrality": nx.closeness_centrality(G),  # 接近中心性
    "betweenness_centrality": nx.betweenness_centrality(G),  # 介数中心性
}

# 将分析结果保存到 JSON 文件
output_file = "graph_analysis_results.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, ensure_ascii=False, indent=4)

print(f"分析结果已保存到 {output_file}")