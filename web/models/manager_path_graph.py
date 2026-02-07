import pandas as pd

"""
PathGraphManager

private:


public:   

"""

path_graph_form = {
    "node": "int",      # 当前单词节点
    "root": "int",      # 根词（step=-1），每个单词只有一个根词
    "step0": "string",                # 同根词（对称），存储为JSON数组
    "step1": "string",                # 同根不同义（非对称），存储为JSON数组
    "step2": "string",                # 近义词（对称），存储为JSON数组
    "step3": "string",                # 反义词（对称），存储为JSON数组  
    "step4": "string",                # 形近词/音近词（对称），存储为JSON数组
}


step_descriptions = {
    -1: "根词关系",
    0: "同根词（意义相同）",
    1: "同根不同义",
    2: "近义词", 
    3: "反义词",
    4: "形近词/音近词"
}

class PathGraphManager:
    def __init__(self):
        self.graph_path = "./Assets/path_graph.csv"

        self.graph = pd.read_csv(self.graph_path, dtype=path_graph_form) # type: ignore

    def get_graph_info(self):
        graph = []
        for _, row in self.graph.iterrows():
            graph.append({
                "node": row["node"],
                "root": row["root"],
                "step0": row["step0"],                # 同根词（对称），存储为JSON数组
                "step1": row["step1"],                # 同根不同义（非对称），存储为JSON数组
                "step2": row["step2"],                # 近义词（对称），存储为JSON数组
                "step3": row["step3"],                # 反义词（对称），存储为JSON数组  
                "step4": row["step4"],                # 形近词/音近词（对称），存储为JSON数组
            })

        return graph
