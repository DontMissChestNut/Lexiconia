import pandas as pd
from datetime import datetime, timedelta
from models import WordRepositoryManager

TEFC  = ("5min", "30min", "12h", "1d", "2d", "4d", "7d", "15d")  # 8 nodes

word_to_review_form = {
    "Root": "-",
    "Word": "-",
    "CurNode": -1,
    "CurTime": "YYYY-MM-DD-hh-mm-ss",
    "NextTime": "YYYY-MM-DD-hh-mm-ss"
}

class MyReviewManager:
    def __init__(self):
        self.review_path = "LexiconiaApp/data/my_review_copy.csv" # test
        # self.review_path = "LexiconiaApp/data/my_review.csv"

        self.word_repo = pd.read_csv('LexiconiaApp/data/word_repository_manager.csv')
        # self.word_repo = pd.read_csv('LexiconiaApp/data/my_review.csv') 
        self.my_review = pd.read_csv(self.review_path)
        
        # 定义时间间隔映射
        self.interval_mapping = {
            "5min": timedelta(minutes=5),
            "30min": timedelta(minutes=30),
            "12h": timedelta(hours=12),
            "1d": timedelta(days=1),
            "2d": timedelta(days=2),
            "4d": timedelta(days=4),
            "7d": timedelta(days=7),
            "15d": timedelta(days=15)
        }

    def new_word(self, word:str):
        """
        新增一个单词到复习列表
        """
        # TODO:更新为交给word_repo管理
        root = self.word_repo["Num"][self.word_repo["WordB"] == word].values[0] if self.word_repo[self.word_repo["WordB"] == word].values.size > 0 else None

        if root is None:
            # TODO: 单词库中不存在，提示用户
            return 0
        elif root is not None and root not in self.my_review["Root"].values:
            # 单词库中存在，不在复习列表，更新到复习列表
            new_word = {
                "Root": "{:0>6d}".format(root),   
                "Word": word,
                "CurNode": -1,
                "CurTime": "YYYY-MM-DD-hh-mm-ss",
                "NextTime": "YYYY-MM-DD-hh-mm-ss",
            }
            wordf = pd.DataFrame([new_word], columns=word_to_review_form.keys())
            wordf.to_csv(self.review_path, mode="a", index=False, header=False, encoding="utf-8")
            return 1
        elif root in self.my_review["Root"].values:
            # TODO: 已存在在复习列表，修改复习状态
            # 直接重制？倒退？不修改？
            return 2
    
    def new_words_web(self, words:list):
        """
        新增一组单词到复习列表
        """
        false_words = []
        added_words = []
        skipped_words = []

        for word in words:
            result = self.new_word(word)
            if result == 0:
                false_words.append(word)
            elif result == 1:
                added_words.append(word)
            elif result == 2:
                skipped_words.append(word)

        return false_words, added_words, skipped_words
    
    def add_review_tasks(self, count:int):
        """
        返回所有待添加到复习表的单词（node为-1）
        count部分由flashcard_service控制
        """
        
        pending_words = self.my_review[self.my_review["CurNode"] == -1]
        
        return pending_words
    
    def update_cur_node(self, row_index, row, tar_node: int):
        """更新单个单词的当前节点"""

        # print(row)

        if row["CurNode"] < 0:     # 还没开始复习
            self.my_review.at[row_index, "CurNode"] = tar_node
            self.my_review.at[row_index, "CurTime"] = "0000-00-00-00-00-00"
            self.my_review.at[row_index, "NextTime"] = "0000-00-00-00-00-00"
        
        if tar_node > 0 and tar_node - 1 < len(TEFC):       # 已经开始复习，并且复习节点在TEFC范围内
            current_time = self.get_current_time()
            interval_key = TEFC[tar_node - 1]  # 获取对应的时间间隔
            next_time = self.calculate_next_time(current_time, interval_key)
            
            # 更新DataFrame - 按照索引更新
            self.my_review.at[row_index, "CurNode"] = tar_node
            self.my_review.at[row_index, "CurTime"] = current_time
            self.my_review.at[row_index, "NextTime"] = next_time
            
        # 保存到CSV
        self.my_review.to_csv(self.review_path, index=False, encoding="utf-8")
    
    def update_cur_nodes(self, roots: list, tar_node: int):
        """批量更新多个单词的当前节点"""
        to_update = self.my_review[self.my_review["Root"].isin(roots)]
        
        for index, row in to_update.iterrows():
            self.update_cur_node(index, row, tar_node)
        # df.to_csv(self.review_path, mode="w", index=False, header=True, encoding="utf-8")

    def get_due_reviews(self):
        """获取到期的复习任务"""
        current_time = datetime.now()
        due_reviews = []
        
        for _, row in self.my_review.iterrows():
            try:
                next_time = datetime.strptime(row["NextTime"], "%Y-%m-%d-%H-%M-%S")
                if next_time <= current_time:
                    due_reviews.append(row)
            except ValueError:
                # 处理时间格式错误的情况
                continue
                
        return pd.DataFrame(due_reviews)    
    
    def get_current_time(self):
        """获取当前时间并格式化为 YYYY-MM-DD-HH-MM-SS"""
        return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def calculate_next_time(self, current_time_str, interval_key):
        """根据当前时间和间隔计算下一次复习时间"""
        if interval_key not in self.interval_mapping:
            return current_time_str
            
        current_time = datetime.strptime(current_time_str, "%Y-%m-%d-%H-%M-%S")
        interval = self.interval_mapping[interval_key]
        next_time = current_time + interval
        return next_time.strftime("%Y-%m-%d-%H-%M-%S")
        