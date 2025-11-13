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

        self.my_review = pd.read_csv(self.review_path,
                                     encoding="utf-8",
                                     header=0)

    def new_word(self, word:str):
        """
        新增一个单词到复习列表
        """
        root = self.word_repo["Num"][self.word_repo["WordB"] == word].values[0] if self.word_repo[self.word_repo["WordB"] == word].values.size > 0 else None
        print(root)

        if root is None:
            return "单词不在单词库哦！"
        elif root is not None and root not in self.my_review["Root"].values:
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

    
    def new_words(self, words:list):
        """
        新增一组单词到复习列表
        """
        current_words_review = self.my_review["Word"].tolist()      # current review
        new_words = []
        for word in words:
            if word in current_words_review:        # in review list, update           
                # Todo: 已存在，更新
                pass
            else:
                new_words.append(word)

        new_words = self.word_repo[self.word_repo["Num"].isin(new_words)]

        return new_words
    
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