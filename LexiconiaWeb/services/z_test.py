from models import WordRepositoryManager, MyReviewManager, CardDetailsManager
from path_graph_manager import PathGraphManager

class LexiconiaService:
    """单词卡业务逻辑服务"""
    
    def __init__(self):
        self.word_repo = WordRepositoryManager()
        self.detail_manager = CardDetailsManager()
        self.review_manager = MyReviewManager()
        self.path_graph = PathGraphManager()
    
    # ... 保持现有方法不变 ...
    
    """ =============== Path Builder 功能 =============== """
    
    def get_word_connections(self, root):
        """获取单词的所有连接关系"""
        connections = self.path_graph.graph[
            (self.path_graph.graph["root"] == root) | 
            (self.path_graph.graph["point"] == root)
        ]
        
        result = []
        for _, conn in connections.iterrows():
            if conn["root"] == root:
                direction = "outgoing"
                target = conn["point"]
            else:
                direction = "incoming" 
                target = conn["root"]
            
            # 获取目标单词信息
            target_word = self.word_repo.word_repo[
                self.word_repo.word_repo["num"] == target
            ]["word_b"].values[0] if not self.word_repo.word_repo[
                self.word_repo.word_repo["num"] == target
            ].empty else "Unknown"
                
            result.append({
                "root": conn["root"],
                "point": conn["point"],
                "step": int(conn["step"]),
                "direction": direction,
                "target_word": target_word,
                "target_root": target
            })
        
        return result
    
    def add_word_connection(self, root, point, step):
        """添加单词连接关系"""
        # 检查连接是否已存在
        existing = self.path_graph.graph[
            (self.path_graph.graph["root"] == root) & 
            (self.path_graph.graph["point"] == point)
        ]
        
        if not existing.empty:
            return False, "连接关系已存在"
        
        # 添加新连接
        new_connection = {
            "root": f"{int(root):06d}",
            "point": f"{int(point):06d}",
            "step": step
        }
        
        new_df = pd.DataFrame([new_connection])
        new_df.to_csv(self.path_graph.graph_path, mode="a", index=False, header=False, encoding="utf-8")
        
        # 重新加载数据
        self.path_graph.graph = pd.read_csv(self.path_graph.graph_path, dtype=self.path_graph.path_graph_form)
        
        return True, "连接关系添加成功"
    
    def delete_word_connection(self, root, point):
        """删除单词连接关系"""
        # 过滤掉要删除的连接
        self.path_graph.graph = self.path_graph.graph[
            ~((self.path_graph.graph["root"] == root) & 
              (self.path_graph.graph["point"] == point))
        ]
        
        # 保存回文件
        self.path_graph.graph.to_csv(self.path_graph.graph_path, index=False, encoding="utf-8")
        
        return True, "连接关系删除成功"
    
    def search_words(self, keyword):
        """搜索单词"""
        if not keyword:
            return []
        
        # 在单词库中搜索
        words = self.word_repo.word_repo[
            (self.word_repo.word_repo["word_a"].str.contains(keyword, case=False, na=False)) |
            (self.word_repo.word_repo["word_b"].str.contains(keyword, case=False, na=False))
        ].head(20)  # 限制返回数量
        
        result = []
        for _, word in words.iterrows():
            result.append({
                "root": word["num"],
                "word": word["word_b"],
                "serial": word["serial"]
            })
        
        return result
    
    def get_word_info(self, root):
        """获取单词详细信息"""
        word_info = self.word_repo.word_repo[
            self.word_repo.word_repo["num"] == root
        ]
        
        if word_info.empty:
            return None
        
        word_data = word_info.iloc[0]
        details = self.detail_manager.get_youdao_details_by_root(root)
        
        return {
            "root": root,
            "word": word_data["word_b"],
            "word_a": word_data["word_a"],
            "serial": word_data["serial"],
            "details": details,
            "connections": self.get_word_connections(root)
        }