from models import WordRepositoryManager
from models import MyReviewManager
from models import CardDetailsManager

class FlashcardService:
    """单词卡业务逻辑服务"""
    
    def __init__(self):
        self.word_repo = WordRepositoryManager()
        self.card_details = CardDetailsManager()
        self.review_manager = MyReviewManager()
    
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
        card_definitions = self.card_details.get_definitions_by_root(num)
        
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
    
    """ =============== 复习 =============== """
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

    # 准备今日复习列表。获取状态为-1的单词，确认是否添加
    def prepare_my_review(self, count:int):
        pending_words = self.review_manager.add_review_tasks(count)

        # 随机选择指定数量的单词
        if len(pending_words) < count:
            sample_words = pending_words
        else:
            sample_words = pending_words.sample(count)
            
        # sample_words["Detail"] = [self.card_details.details["Root"] == sample_words["Root"]]
        
        words = []
        for _, row in sample_words.iterrows():
            words.append({
                "Root": row["Root"],
                "Word": row["Word"],
                "Details": self.card_details.get_details_by_root(row["Root"])
            })
            
        
        # print(words)
            
        return words
    
    # 更新选中单词的状态
    def update_view_status_nodes(self, roots:list, target_node:int):
        self.review_manager.update_cur_nodes(roots, target_node)
            

    # 检查值是否有效（不为空、NaN或'-'）
    def _is_valid_value(self, value):
        """检查值是否有效（不为空、NaN或'-'）"""
        import pandas as pd
        return pd.notna(value) and value != '' and value != '-'
    