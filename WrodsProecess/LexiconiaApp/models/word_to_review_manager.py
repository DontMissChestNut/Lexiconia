import pandas as pd
from models import WordRepositoryManager

TEFC  = ("5min", "30min", "12h", "1d", "2d", "4d", "7d", "15d")  # 8 nodes

word_to_review_form = {
    "Root": "-",
    "Serial": "-",                      # 序列：无效
    "Word": "-",                        # 单词：无效
    "CurNode": "(-2,)",                 # 有误，处理为整数
    "CurTime": "YYYY-MM-DD-hh-mm-ss",
    "NextTime": "YYYY-MM-DD-hh-mm-ss",
}

class WordToReviewManager:
    def __init__(self):
        self.review_path = "LexiconiaApp/data/word_to_review.csv"
        self.repository_manager = WordRepositoryManager()

        self.word_review = pd.read_csv(self.review_path, dtype=word_to_review_form)

    def new_word(self, words:list):
        
        current_words_review = self.word_review["Word"].tolist()      # current review
        new_words = []
        for word in words:
            if word in current_words_review:        # in review list, update           
                # Todo: 已存在，更新
                pass
            else:
                new_words.append(word)

        new_words = self.repository_manager.generate_new_words(new_words)

        return new_words
    
    def add_review_tasks(self, words:list):
        new_tasks = []
        for word in words:
            new_tasks.append({
                "Root": word["Num"],
                "Serial": "-",                      # 序列：无效
                "Word": word,                        # 单词：无效
                "CurNode": "(-2,)",                 # 有误，处理为整数
                "CurTime": "YYYY-MM-DD-hh-mm-ss",
                "NextTime": "YYYY-MM-DD-hh-mm-ss",
            })

        tasksf = pd.DataFrame(columns=word_to_review_form.keys())
        tasksf = pd.concat([tasksf, pd.DataFrame(tasks)], ignore_index=True)
        tasksf.to_csv(self.review_path, mode="a", index=False, header=False, encoding="utf-8")
