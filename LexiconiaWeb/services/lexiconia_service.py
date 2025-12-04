import pandas as pd
from models import WordRepositoryManager, MyReviewManager, CardDetailsManager, PathGraphManager

class LexiconiaService:
    """单词卡业务逻辑服务"""
    
    def __init__(self):
        self.word_repo = WordRepositoryManager()
        self.detail_manager = CardDetailsManager()
        self.review_manager = MyReviewManager()
        self.path_graph = PathGraphManager()

    
    """ =============== daily review =============== """
    # 获取每日复习单词
    def get_daily_reviews(self, repo: str = 'youdao'):
        """获取每日复习单词"""

        due_roots = self.review_manager.get_due_reviews()

        print(f"due_roots: {due_roots}")
        wordlist = self.word_repo.get_words_by_roots(due_roots)

        youdao_details = []
        for word in wordlist:
            # TODO: select repo by param
            details = self.detail_manager.get_youdao_details_by_root(word[0])
            detail = []
            for d in details:
                # print(d["Addition"])
                detail.append({
                    "Level": d["Level"],
                    "part_of_speech": d["part_of_speech"],
                    "Addition": d["Addition"],                # 名词复数、动词变形等
                    "ExplainationC": d["ExplainationC"]
                })
            youdao_details.append({
                "Root": word[0],
                "Word": word[1],
                "Details": detail
            })
        
        return youdao_details

    # 获取单词卡数据
    def get_card_data(self, num=None):
        """获取单词卡数据"""
        import random
        
        # 如果未指定序列号，随机选择一个
        if num is None:
            all_nums = self.word_repo.get_all_nums()
            if not all_nums:
                return None
            num = random.choice(all_nums)
        
        # 获取单词基本信息
        word_data = self.word_repo.get_word_by_num(num)
        if word_data is None:
            return None
        
        # 获取单词的多个释义
        card_definitions = self.detail_manager.get_definitions_by_root(num)
        
        definitions_list = []
        for _, definition in card_definitions.iterrows():
            definitions_list.append({
                'level': definition['Level'],
                'part_of_speech': definition['part_of_speech'],
                'addition': definition['addition'] if self._is_valid_value(definition['addition']) else '',
                'explanation_e': definition['ExplainationE'] if self._is_valid_value(definition['ExplainationE']) else '',
                'explanation_c': definition['ExplainationC'] if self._is_valid_value(definition['ExplainationC']) else '',
                'example': definition['Example'] if self._is_valid_value(definition['Example']) else ''
            })
        
        return {
            'word': word_data['WordB'],
            'num': num,
            'definitions': definitions_list
        }
    
    # 添加多个单词
    def add_words(self, words_string):
        """添加多个单词"""
        words_list = [word.strip() for word in words_string.split(',') if word.strip()]
        added_words, skipped_words = self.word_repo.add_words_batch(words_list)
        
        return {
            'added': [word for word in added_words],
            'skipped': skipped_words,
            'added_count': len(added_words),
            'skipped_count': len(skipped_words)
        }
    
    # 获取所有卡片序列号
    def get_all_cards(self):
        """获取所有卡片序列号"""
        return self.word_repo.get_all_nums()
    
    """ =============== Prepare Review Words =============== """
    # multi: 向复习仓库添加复习单词
    def add_my_review(self, words:list):
        """向复习仓库添加复习单词"""
        false_words, added_words, skipped_words = self.review_manager.new_words_web(words)

        return {
            'false': false_words,
            'added': added_words,
            'skipped': skipped_words,
            'false_count': len(false_words),
            'added_count': len(added_words),
            'skipped_count': len(skipped_words)
        }

    # 准备今日复习列表。获取状态为-1的单词，确认是否添加到今日复习列表
    def prepare_my_review(self, count:int, repo:str):
        """
        准备今日复习列表
        仅从review list里获取 root-word-details
        
        Args:
            count (int): 今日复习单词数量
        """
        pending_words = self.review_manager.add_review_tasks(count)

        # 随机选择指定数量的单词
        if len(pending_words) < count:
            sample_words = pending_words
        else:
            sample_words = pending_words.sample(count)
            
        # sample_words["Detail"] = [self.detail_manager.details["Root"] == sample_words["Root"]]
        roots = [i for i in sample_words["Root"]]

        self.detail_manager.update_youdao_details(roots)

        words = []
        for _, row in sample_words.iterrows():
            words.append({
                "Root": row["Root"],
                "Word": row["Word"],
                "Details": self.detail_manager.get_details_by_root(row["Root"]) if repo == "complex" else self.detail_manager.get_youdao_details_by_root(row["Root"])
            })
            
        return words
    
    def prepare_my_review_youdao(self, count:int):
        """准备今日复习列表
        
        Args:
            count (int): 今日复习单词数量
        """
        pending_words = self.review_manager.add_review_tasks(count)

        # 随机选择指定数量的单词
        if len(pending_words) < count:
            sample_words = pending_words
        else:
            sample_words = pending_words.sample(count)
            
        # sample_words["Detail"] = [self.detail_manager.details["Root"] == sample_words["Root"]]
        # print(sample_words["Root"])

        # 检查是否待添加单词详情完整
        self.detail_manager.update_youdao_details(sample_words["Root"])
        
        words = []
        for _, row in sample_words.iterrows():
            words.append({
                "Root": row["Root"],
                "Word": row["Word"],
                "Details": self.detail_manager.get_youdao_details_by_root(row["Root"])
            })
            
        return words
    
    # 更新选中单词的状态
    def update_view_status_nodes(self, roots:list):
        """更新选中单词的状态"""
        return self.review_manager.update_cur_nodes(roots)
            
    # 将传入的root序列单词复习节点改为0，可以准备开始复习
    def start_review_0(self, root:list):
        
        count = self.review_manager.update_cur_nodes_tar(root, 0)
        
        return count
    
    
    """ =============== Path Builder =============== """
    """ multy:获取单词的根 """
    def get_num(self, word:list):
        nums = [_["Num"] for _ in self.word_repo.generate_words_num(word)]
        return int(nums[0])
    
    def get_graph_info(self):
        graph = self.path_graph.get_graph_info()
        word_list = self.word_repo.generate_word_list()
        return graph, word_list
    
    """ =============== Daily Update =============== """
    def daily_update(self):
        self.review_manager.daily_update()

    # 检查值是否有效（不为空、NaN或'-'）
    def _is_valid_value(self, value):
        """检查值是否有效（不为空、NaN或'-'）"""
        import pandas as pd
        return pd.notna(value) and value != '' and value != '-'
    