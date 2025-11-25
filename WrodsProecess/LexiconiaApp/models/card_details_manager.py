import pandas as pd

"""
CardDetailsManager

- Complex Card Details
-- 添加卡片详情
-- 删除卡片详情
-- 重写卡片详情（更新）
-- 获取单词的卡片详情

- Youdao Card Details
-- 添加卡片详情
-- multi: 添加卡片详情
-- 删除卡片详情
-- TODO：重写卡片详情（更新）
-- 获取单词的卡片详情
-- ？：更新详情，跟重写有什么区别？
"""

word_card_form= {
    "Root": "string",
    "Serial" : "string",
    "Level": "string",
    "part_of_speech": "00-000000-00-0",        # CEFR(0)+level - root - part of speech - num
    "Addition": "string",           # 名词复数、动词变形等
    "ExplainationE": "string",
    "ExplainationC": "string",
    # "Phonetic": "string"          # TODO： 音标
}

word_card_form_youdao= {
    "Root": "string",
    "Serial" : "10-000000-00-0",        # youdao(1)+level - root - part of speech - num
    "Level": "string",
    "part_of_speech": "string",
    "Addition": "string",           # 名词复数、动词变形等
    "ExplainationE": "string",
    "ExplainationC": "string",
    # "Phonetic": "string"          # TODO： 音标
}

Level = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
    "-":  9
}

PartofSpeech = {
    "adjective":        1,
    "adverb":           2,
    "auxiliary verb":   3,
    "conjunction":      4, 
    "determiner":       5,
    "exclamation":      6,
    "modal verb":       7,
    "noun":             8,
    "number":           9,
    "preposition":      10,
    "pronoun":          11,
    "verb":             12,
    "phrase":           21,
    "phrasal verb":     22,
}

class CardDetailsManager:
    def __init__(self):
        self.detail_path = "LexiconiaApp/data/card_details.csv"
        self.detail_youdao_path = "LexiconiaApp/data/card_details_youdao_test.csv"
        # self.detail_youdao_path = "LexiconiaApp/data/card_details_youdao.csv"
        
        self.details = pd.read_csv(self.detail_path)
        self.details_youdao = pd.read_csv(self.detail_youdao_path)

    def _update_details(self):
        """读取内容"""
        self.details = pd.read_csv(self.detail_path)
        self.details_youdao = pd.read_csv(self.detail_youdao_path)
        return


    """ =============== Complex Card Details =============== """
    # 添加卡片详情
    def add_card_detail(self, card_detail: dict):
        """添加卡片详情"""
        cardf = pd.DataFrame([card_detail], columns=word_card_form.keys())
        cardf.to_csv(self.detail_path, mode="a", index=False, header=False, encoding="utf-8")
        
        self._update_details()
        return

    # 删除卡片详情
    def erase_card_detail(self, serial: str):
        """删除卡片详情"""
        df = pd.read_csv(self.detail_path, encoding="utf-8", header=0)
        df = df[df["Serial"] != serial]
        df.to_csv(self.detail_path, mode="w", index=False, header=True, encoding="utf-8")
        
        self._update_details()
        return
    
    # 重写卡片详情 （更新）
    def rewrite_card_detail(self, card_detail: dict, serial: str):
        """重写卡片详情"""
        df = pd.read_csv(self.detail_path, encoding="utf-8", header=0)
        df = df[df["Serial"] != serial]
        df.to_csv(self.detail_path, mode="w", index=False, header=True, encoding="utf-8")
        self.add_card_detail(card_detail)

        self._update_details()
        return

    # 获取单词的卡片详情
    def get_details_by_root(self, root:int):
        """获取单词的卡片详情"""

        details = []
        for _, row in self.details[ self.details["Root"] == root].iterrows():
            details.append({
                # TODO："Phonetic": "string",
                "Level": row["Level"],
                "part_of_speech": row["part_of_speech"],
                "Addition": row["Addition"],                # 名词复数、动词变形等
                "ExplainationE": row["ExplainationE"],
                "ExplainationC": row["ExplainationC"]
            })
            
        print(details)
        
        return details
    
    """ =============== Youdao Card Details =============== """
    # 添加卡片详情
    def add_card_detail_youdao(self, card_detail: dict):
        """添加卡片详情"""
        cardf = pd.DataFrame([card_detail], columns=word_card_form_youdao.keys())
        cardf.to_csv(self.detail_youdao_path, mode="a", index=False, header=False, encoding="utf-8")
        
        self._update_details()
        return
    
    # multi: 添加卡片详情
    def add_card_details_youdao(self, card_details: list):
        """添加卡片详情"""
        print(card_details)

        data = []
        for detail in card_details:
            if detail:
                for i in [_ for _ in detail]:
                    data.append(i)

        cardf = pd.DataFrame(data, columns=word_card_form_youdao.keys())
        cardf.to_csv(self.detail_youdao_path, mode="a", index=False, header=False, encoding="utf-8")
        
        self._update_details()
        return

    # 删除卡片详情
    def erase_card_detail_youdao(self, serial: str):
        """删除卡片详情"""
        df = pd.read_csv(self.detail_youdao_path, encoding="utf-8", header=0)
        df = df[df["Serial"] != serial]
        df.to_csv(self.detail_youdao_path, mode="w", index=False, header=True, encoding="utf-8")
        
        self._update_details()
        return
    
    # TODO：重写卡片详情（更新）
    def rewrite_card_detail_youdao(self, card_detail: dict, serial: str):
        """重写卡片详情"""
        
        return
    
    # 获取单词的有道卡片详情
    def get_youdao_details_by_root(self, root:int):
        details = []
        for _, row in self.details_youdao[ self.details_youdao["Root"] == root].iterrows():
            details.append({
                # TODO："Phonetic": "string",
                "Level": row["Level"],
                "part_of_speech": row["part_of_speech"],
                "Addition": row["Addition"],                # 名词复数、动词变形等
                "ExplainationE": row["ExplainationE"],
                "ExplainationC": row["ExplainationC"]
            })
        
        return details
    
        # 查询详情是否已添加
    
    # 更新详情
    def update_youdao_details(self, roots: list):
        from models import Crawler
        crawler = Crawler()
        added, not_added = self._is_youdao_detail_added(roots)
        if len(not_added) > 0:
            details = crawler.crawl(not_added)
            self.add_card_details_youdao(details)

        self._update_details()
        return "{} added, {} not added".format(len(added), len(not_added))
    
    # 查询详情是否已添加
    def _is_youdao_detail_added(self, roots: list):
        """
        查询详情是否已添加
        
        Args:
            root (list): A list of roots to query. Root is insured to be exist in the word repository in previous process
        
        Returns:
            added(list): A list of serials that are added
            not_added(list): A list of serials that are not added
        """
        added = []
        not_added = []
        for r in roots:
            if r in self.details_youdao["Root"].values:
                added.append(r)
            else:
                not_added.append(r)
        return added, not_added
            