import pandas as pd
from datetime import datetime, timedelta, time
from models import WordRepositoryManager

"""
MyReviewManager 管理单词的复习列表

"""
# TODO：新增 -0min- 节点
TEFC  = ("5min", "30min", "12h", "1d", "2d", "4d", "7d", "15d")  # 8 nodes

word_to_review_form = {
    "root": "-",
    "Word": "-",
    "CurNode": -1,
    "CurTime": "YYYY-MM-DD-hh-mm-ss",
    "NextTime": "YYYY-MM-DD-hh-mm-ss"
}

class MyReviewManager:
    def __init__(self):
        self.updateTime = time(5, 0, 0)  # 05:00:00

        # self.word_repo_path = "../Assets/word_repository_copy.csv"   # test
        # self.review_path = "../Assets/my_review_copy.csv" # test
        self.word_repo_path = "./Assets/word_repository.csv"
        self.review_path = "./Assets/my_review.csv"

        self.word_repo = pd.read_csv(self.word_repo_path)
        self.my_review = pd.read_csv(self.review_path)
        
        # 定义时间间隔映射
        self.interval_mapping = {
            "0min": timedelta(minutes=0),
            "5min": timedelta(minutes=5),
            "30min": timedelta(minutes=30),
            "12h": timedelta(hours=12),
            """ ----------- frist day ----------- """
            "1d": timedelta(days=1),
            "2d": timedelta(days=2),
            "4d": timedelta(days=4),
            "7d": timedelta(days=7),
            "15d": timedelta(days=15)
        }

    """ single: 新增一个单词到复习列表 """
    def new_word(self, word:str):
        """
        新增一个单词到复习列表
        """
        # TODO:更新为交给word_repo管理
        root = self.word_repo["num"][self.word_repo["word_b"] == word].values[0] if self.word_repo[self.word_repo["word_b"] == word].values.size > 0 else None

        if root is None:
            # TODO: 单词库中不存在，提示用户
            return 0
        elif root is not None and root not in self.my_review["root"].values:
            # 单词库中存在，不在复习列表，更新到复习列表
            new_word = {
                "root": "{:0>6d}".format(root),   
                "Word": word,
                "CurNode": -1,
                "CurTime": "YYYY-MM-DD-hh-mm-ss",
                "NextTime": "YYYY-MM-DD-hh-mm-ss",
            }
            wordf = pd.DataFrame([new_word], columns=list(word_to_review_form.keys()))
            wordf.to_csv(self.review_path, mode="a", index=False, header=False, encoding="utf-8")
            return 1
        elif root in self.my_review["root"].values:
            # TODO: 已存在在复习列表，修改复习状态
            # 直接重制？倒退？不修改？
            return 2
    
    """ multi: 新增一组单词到复习列表 """
    def new_words_web(self, words:list):
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
    
    """ multi: 返回所有待添加到复习表的单词（node为-1） 
    返回所有待添加到复习表的单词（node为-1）
    count部分由lexiconia_service 控制
    """
    def add_review_tasks(self, count:int):
        pending_words = self.my_review[self.my_review["CurNode"] == -1]
        
        return pending_words
    
    """ single: 更新单个单词的当前节点 """
    def update_cur_node(self, row_index, row, tar_node: int):
        """更新单个单词的当前节点"""

        if row["CurNode"] < 0:     # 还没开始复习
            self.my_review.at[row_index, "CurNode"] = tar_node
            self.my_review.at[row_index, "CurTime"] = self._get_current_time()
            self.my_review.at[row_index, "NextTime"] = self._get_current_time()
        
        if tar_node > 0 and tar_node - 1 < len(TEFC):       # 已经开始复习，并且复习节点在TEFC范围内
            current_time = self._get_current_time()
            next_time = self._calculate_next_time(current_time, tar_node)

            # 更新DataFrame - 按照索引更新
            self.my_review.at[row_index, "CurNode"] = tar_node
            self.my_review.at[row_index, "CurTime"] = current_time
            self.my_review.at[row_index, "NextTime"] = next_time
            
        # 保存到CSV
        try:
            self.my_review.to_csv(self.review_path, index=False, encoding="utf-8")
            return True
        except Exception as e:
            return False
    
    """ single: 更新单词的当前节点 """
    def update_cur_nodes(self, roots: list):
        """批量更新多个单词的当前节点"""
        try:
            to_update = self.my_review[self.my_review["root"].isin(roots)]

            for index, row in to_update.iterrows():
                self.update_cur_node(index, row, int(row["CurNode"]) + 1)
            
            return True
        except Exception as e:
            return False
    
    """ multi: 批量更新多个单词的当前节点 """
    def update_cur_nodes_tar(self, roots: list, tar_node: int):
        to_update = self.my_review[self.my_review["root"].isin(roots)]
        
        count = 0
        for index, row in to_update.iterrows():
            self.update_cur_node(index, row, tar_node)
            count += 1
        
        return count
    
    """multi: 获取到期的复习任务，返回到期的单词root list
    根据时间排序，早 -> 晚
    TODO：0-2阶段考虑时分秒信息，其他阶段只考虑日期
    """
    def get_due_reviews(self):
        current_time = datetime.now()
        due_roots = []
        
        for _, row in self.my_review.iterrows():            
            if row["CurNode"] < 0:
                continue
            try:
                
                next_time = datetime.strptime(row["NextTime"], "%Y-%m-%d-%H-%M-%S")

                if next_time <= current_time:
                    due_roots.append({"root": row["root"], "NextTime": row["NextTime"]})
            except ValueError:
                # 处理时间格式错误的情况
                continue
        due_roots.sort(key=lambda x: x["NextTime"])

        """ sort by NextTime, from early to late"""
        result = set(item["root"] for item in due_roots)        

        return result
    
    """daily update at 05:00, current_node < 3 upto 3"""
    def daily_update(self):
        self.my_review = pd.read_csv(self.review_path)

        for _, row in self.my_review.iterrows():
            if (int(row["CurNode"]) < 3 and int(row["CurNode"]) > 0):
                # 更新DataFrame - 按照索引更新
                self.my_review[_, "CurNode"] = 3
            
                # 保存到CSV
                self.my_review.to_csv(self.review_path, index=False, encoding="utf-8")
    """ daily_update_abolished
    def daily_update_abolished(self):
        self.my_review = pd.read_csv(self.review_path)

        for _, row in self.my_review.iterrows():
            if (int(row["CurNode"]) < 3 and int(row["CurNode"]) > 0):
                current_date = datetime.now().date()
                fixed_time = self.updateTime

                tar_node = 3
                next_time = datetime.combine(current_date, fixed_time)
                

                # 更新DataFrame - 按照索引更新
                self.my_review.at[_, "CurNode"] = tar_node
                self.my_review.at[_, "NextTime"] = next_time
            
                # 保存到CSV
                self.my_review.to_csv(self.review_path, index=False, encoding="utf-8")
    """

    """获取当前时间并格式化为 YYYY-MM-DD-HH-MM-SS"""
    def _get_current_time(self):
        """获取当前时间并格式化为 YYYY-MM-DD-HH-MM-SS"""
        return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def _calculate_next_time(self, current_time_str, tar_node: int):

        interval_key = TEFC[tar_node - 1]  # 获取对应的时间间隔

        """根据当前时间和间隔计算下一次复习时间"""
        if interval_key not in self.interval_mapping:
            return current_time_str
            
        current_time = datetime.strptime(current_time_str, "%Y-%m-%d-%H-%M-%S")
        interval = self.interval_mapping[interval_key]
        

        next_time = current_time + interval

        if tar_node > 3:  
            next_date = next_time.date()
            fixed_time = self.updateTime
            next_time = datetime.combine(next_date, fixed_time)

        
        return next_time.strftime("%Y-%m-%d-%H-%M-%S")
        
    