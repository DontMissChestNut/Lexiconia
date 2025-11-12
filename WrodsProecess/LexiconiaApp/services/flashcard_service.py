from models import WordRepositoryManager
from models import CardDetailsManager

class FlashcardService:
    """单词卡业务逻辑服务"""
    
    def __init__(self):
        self.word_repo = WordRepositoryManager()
        self.card_details = CardDetailsManager()
    
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
                'part_of_speech': definition['Part of Speech'],
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
    
    def get_all_cards(self):
        """获取所有卡片序列号"""
        return self.word_repo.get_all_nums()
    
    def _is_valid_value(self, value):
        """检查值是否有效（不为空、NaN或'-'）"""
        import pandas as pd
        return pd.notna(value) and value != '' and value != '-'