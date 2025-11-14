import pandas as pd
from models import WordRepositoryManager

TEFC  = ("5min", "30min", "12h", "1d", "2d", "4d", "7d", "15d")  # 8 nodes

word_to_review_form = {
    "Root": "-",
    "Serial": "-",                      # 序列：无效
    "Word": "-",                        # 单词：无效
    "CurNode": -2,                      # 有误，处理为整数
    "CurTime": "YYYY-MM-DD-hh-mm-ss",
    "NextTime": "YYYY-MM-DD-hh-mm-ss",
}

class MyReviewManager:
    def __init__(self):
        self.review_path = "LexiconiaApp/data/my_review.csv"
        self.word_repo = pd.read_csv('LexiconiaApp/data/word_repository.csv')

        self.my_review = pd.read_csv(self.review_path)

    def new_word(self, word:str):
        """
        新增一个单词到复习列表
        """
        root = self.word_repo["Num"][self.word_repo["WordB"] == word].values[0] if self.word_repo[self.word_repo["WordB"] == word].values.size > 0 else None

        if root is None:
            # TODO: 单词库中不存在，提示用户
            return 0
        elif root is not None and root not in self.my_review["Root"].values:
            # 单词库中存在，不在复习列表，更新到复习列表
            new_word = {
                "Root":root,
                "Serial": "-",                          # 序列：无效
                "Word": "-",                            # 单词：无效    
                "CurNode": -2,                          # 有误，处理为整数
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

        added_words = self.word_repo[self.word_repo["Num"].isin(added_words)]

        return false_words, added_words, skipped_words
    
    def add_review_tasks(self, words:list):
        new_tasks = []
        for word in words:
            new_tasks.append({
                "Root": word["Num"],
                "Serial": "-",                          # 序列：无效
                "Word": "-",                            # 单词：无效
                "CurNode": -2,                          # 有误，处理为整数
                "CurTime": "YYYY-MM-DD-hh-mm-ss",
                "NextTime": "YYYY-MM-DD-hh-mm-ss",
            })

        tasksf = pd.DataFrame(columns=word_to_review_form.keys())
        tasksf = pd.concat([tasksf, pd.DataFrame(new_tasks)], ignore_index=True)
        tasksf.to_csv(self.review_path, mode="a", index=False, header=False, encoding="utf-8")