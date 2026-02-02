import pandas as pd
from models import CardDetailsManager

"""
WordRepositoryManager
private:
- single:添加新单词

public:   
- single:创建单词信息
- multi:创建单词信息
- single:添加单词到单词库
- multi:添加单词到单词库
- multi:根据单词获取单词num
- multi:根据 root 获取 单词（仅单词）
- multi:分批处理，返回添加和跳过的单词列表
"""

word_repository_form = {
    "Num": "string",
    "serial" : "string",
    "WordB": "string",
    "WordA": "string",

}

class WordRepositoryManager:
    def __init__(self):
        self.repository_path = "./Assets/word_repository.csv"
        self.details_manager = CardDetailsManager()

        self.word_repo = pd.read_csv(self.repository_path, dtype=word_repository_form)

    # single:添加新单词
    def _add_new_word(self, word_detail: dict):
        """添加新单词"""
        wordf = pd.DataFrame([word_detail], columns=word_repository_form.keys())
        wordf.to_csv(self.repository_path, mode="a", index=False, header=False, encoding="utf-8")

    # single:创建单词信息
    def create_new_word(self, word: str):
        """
        输入单个单词，创建单词信息
        返回是否是新单词，并成功创建单词信息和卡片详情
        """
        word = word.strip()
        words = self.word_repo

        # 判断是否是新单词
        if word not in words["WordA"].values and word not in words["WordB"].values:
            # 新单词，创建单词信息
            # TODO: 区分英式英语和美式英语
            addition_count = len(words) + 342       # 非原生部分从7000开始添加

            new_word = {
                "Num": "{:0>6d}".format(addition_count),
                "serial" : "09-{:0>6d}-01-1".format(addition_count),
                "WordB": word,
                "WordA": word,      # 美式
            }
            
            # 新单词，添加到单词库
            self._add_new_word(new_word)

            # 新单词，创建卡片详情
            self.details_manager.add_card_detail({
                "root": new_word["Num"],
                "serial" : new_word["serial"],
                "level": "-",
                "part_of_speech": "-",
                "addition": "-",
                "ExplainationE": "-",
                "ExplainationC": "-"
            })

            return True
        else:
            return False

    # multi:创建单词信息
    def create_new_words(self, word_list:list):
        """
        输入单词列表，创建单词信息
        """
        words = self.word_repo

        addition_count = len(words) + 342       # 非原生部分从7000开始添加
        
        new_words = []
        for word in word_list:
            if word not in words["WordA"].values and word not in words["WordB"].values:
                new_words.append({
                    "Num": "{:0>6d}".format(addition_count),
                    "serial" : "09-{:0>6d}-01-1".format(addition_count),
                    "WordB": word,
                    "WordA": word,
                })
                addition_count += 1
                
        wlf = pd.DataFrame(columns=word_repository_form.keys())
        wlf = pd.concat([wlf, pd.DataFrame(new_words)], ignore_index=True)
        wlf.to_csv(self.repository_path, mode="a", index=False, header=False, encoding="utf-8")
        return new_words

    # single:添加单词到单词库
    def add_word_repository(self, word: str):
        """
        输入单词，添加到单词库
        """
        word = word.strip()
        self.create_new_word(word)

    # multi:添加单词到单词库
    def add_words_repository(self, line: str):
        """
        通过长string添加到单词库
        """
        words = line.split(",")
        
        # TODO: 处理短语，移除前后空格后仍包含空格，则为短语
        # word.strip()
        words = [word.replace(" ", "") for word in words]

        new_words = self.create_new_words(words)

        for word in new_words:
            self.details_manager.add_card_detail({
                "root": word["Num"],
                "serial" : word["serial"],
                "level": "-",
                "part_of_speech": "-",
                "addition": "-",
                "ExplainationE": "-",
                "ExplainationC": "-"
            })

    # multi:根据单词获取单词num
    def generate_words_num(self, words:list):
        """
        输入单词列表，获取单词对应的num
        """
        new_words = []
        exist_words = []
        for word in words:
            if word not in self.word_repo["WordA"].values and word not in self.word_repo["WordB"].values:
                new_words.append(word)
            elif word in self.word_repo["WordB"].values:
                exist_words.append({
                    "Num": self.word_repo[self.word_repo["WordB"] == word]["Num"].values[0],
                    "Word": word
                })
            elif word in self.word_repo["WordA"].values:
                exist_words.append({
                    "Num": self.word_repo[self.word_repo["WordA"] == word]["Num"].values[0],
                    "Word": word
                })

        new_words = self.create_new_words(new_words)
        new_words = [{
            "Num": word["Num"],
            "Word": word["WordB"],
        } for word in new_words if word["WordB"]]
        
        words = new_words + exist_words       

        return words
    
    # multi:根据 root 获取 单词（仅单词）
    def get_words_by_roots(self, roots:list):
        """
        根据 root 获取 单词（仅单词）
        """
        words = []
        for root in roots:
            words.append([int(root), self.word_repo[self.word_repo["Num"] == "{:0>6d}".format(int(root))]["WordB"].values[0]])

        return words
        
    # multi:分批处理，返回添加和跳过的单词列表
    def add_words_batch(self, words:list):
        """
        获取网页用户输入单词列表，批量添加单词到单词库
        return:
            新添加的单词列表： added_words: list
            跳过（已存在）的单词列表： skipped_words: list
        """
        cur_words = list(tuple(self.word_repo["WordA"].values.tolist() + self.word_repo["WordB"].values.tolist()))
        
        added_words = []
        skipped_words = []

        for w in words:
            if w not in cur_words:
                self.add_word_repository(w)
                added_words.append(w)
            else:
                skipped_words.append(w)

        return added_words, skipped_words

    # multi: 生成单词列表
    def generate_word_list(self):
        word_list = []
        for _, row in self.word_repo.iterrows():
            word_list.append({int(row["Num"]): row["WordB"]})

        return word_list
