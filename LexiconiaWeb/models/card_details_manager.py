import pandas as pd

""" CardDetailsManager

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
    "root": "string",
    "serial" : "string",
    "level": "string",
    "part_of_speech": "00-000000-00-0",        # CEFR(0)+level - root - part of speech - num
    "addition": "string",           # 名词复数、动词变形等
    "explaination_e": "string",
    "explaination_c": "string",
    # "Phonetic": "string"          # TODO： 音标
}

word_card_form_youdao= {
    "root": "string",
    "serial" : "10-000000-00-0",        # youdao(1)+level - root - part of speech - num
    "level": "string",
    "part_of_speech": "string",
    "addition": "string",           # 名词复数、动词变形等
    "explaination_e": "string",
    "explaination_c": "string",
    # "Phonetic": "string"          # TODO： 音标
}

level = {
    1:"A1",
    2:"A2",
    3:"B1",
    4:"B2",
    5:"C1",
    6:"C2",
    9:"-",
}

PartofSpeech = {
    1:"adjective",        
    2:"adverb",           
    3:"auxiliary verb",   
    4:"conjunction",      
    5:"determiner",       
    6:"exclamation",      
    7:"modal verb",       
    8:"noun",             
    9:"number",           
    10:"preposition",     
    11:"pronoun",         
    12:"verb",            
    21:"phrase",          
    22:"phrasal verb",    
}

class CardDetailsManager:
    def __init__(self):
        self.file_path = "./Assets/card_details.csv"
        # self.file_youdao_path = "./Assets/card_details_youdao_test.csv"
        self.file_youdao_path = "./Assets/card_details_youdao.csv"
        
        self.details = pd.read_csv(self.file_path)
        self.details_youdao = pd.read_csv(self.file_youdao_path)

    def _update_details(self):
        """读取内容"""
        self.details = pd.read_csv(self.file_path)
        self.details_youdao = pd.read_csv(self.file_youdao_path)
        return


    """ =============== Complex Card Details =============== """
    # 添加卡片详情
    def add_card_detail(self, card_detail: dict):
        """添加卡片详情"""
        cardf = pd.DataFrame([card_detail], columns=word_card_form.keys())
        cardf.to_csv(self.file_path, mode="a", index=False, header=False, encoding="utf-8")
        
        self._update_details()
        return

    # 删除卡片详情
    def erase_card_detail(self, serial: str):
        """删除卡片详情"""
        df = pd.read_csv(self.file_path, encoding="utf-8", header=0)
        df = df[df["serial"] != serial]
        df.to_csv(self.file_path, mode="w", index=False, header=True, encoding="utf-8")
        
        self._update_details()
        return
    
    # 重写卡片详情 （更新）
    def rewrite_card_detail(self, card_detail: dict, serial: str):
        """重写卡片详情"""
        df = pd.read_csv(self.file_path, encoding="utf-8", header=0)
        df = df[df["serial"] != serial]
        df.to_csv(self.file_path, mode="w", index=False, header=True, encoding="utf-8")
        self.add_card_detail(card_detail)

        self._update_details()
        return

    # single: 获取单词的卡片详情
    def get_details_by_root(self, root:int):
        """获取单词的卡片详情"""

        details = []
        level = []
        for _, row in self.details[ self.details["root"] == root].iterrows():
            details.append({
                # TODO："Phonetic": "string",
                "level": row["level"],
                "part_of_speech": row["part_of_speech"],
                "addition": row["addition"],                # 名词复数、动词变形等
                "explaination_e": row["explaination_e"],
                "explaination_c": row["explaination_c"]
            })

            level.append(row["level"])
            
        # print(details)
        
        return details
    
    def get_level_by_root(self, root:int):
        """获取单词的卡片详情"""

        level = ""
        for _, row in self.details[ self.details["root"] == root].iterrows():
            level = row["level"]
            
        # print(level)
        
        return level
    
    """ =============== Youdao Card Details =============== """
    # 添加卡片详情
    def add_card_detail_youdao(self, card_detail: dict):
        """添加卡片详情"""
        cardf = pd.DataFrame([card_detail], columns=word_card_form_youdao.keys())
        cardf.to_csv(self.file_youdao_path, mode="a", index=False, header=False, encoding="utf-8")
        
        self._update_details()
        return
    
    # multi: 添加卡片详情
    def add_card_details_youdao(self, card_details: list):
        """添加卡片详情"""
        data = []
        for detail in card_details:
            if detail:
                for i in [_ for _ in detail]:
                    data.append(i)

        cardf = pd.DataFrame(data, columns=word_card_form_youdao.keys())
        cardf.to_csv(self.file_youdao_path, mode="a", index=False, header=False, encoding="utf-8")
        
        self._update_details()
        return

    # 删除卡片详情
    def erase_card_detail_youdao(self, serial: str):
        """删除卡片详情"""
        df = pd.read_csv(self.file_youdao_path, encoding="utf-8", header=0)
        df = df[df["serial"] != serial]
        df.to_csv(self.file_youdao_path, mode="w", index=False, header=True, encoding="utf-8")
        
        self._update_details()
        return
    
    # TODO：重写卡片详情（更新）
    def rewrite_card_detail_youdao(self, card_detail: dict, serial: str):
        """重写卡片详情"""
        
        return
    
    # single：获取单词的有道卡片详情
    def get_youdao_details_by_root(self, root:int):
        details = []
        for _, row in self.details_youdao[ self.details_youdao["root"] == root].iterrows():              
            # print(row)
            details.append({
                # TODO："Phonetic": "string",
                "level": level[int(row["level"])],
                "part_of_speech": row["part_of_speech"],
                "addition": row["addition"],                # 名词复数、动词变形等
                "explaination_e": row["explaination_e"],
                "explaination_c": row["explaination_c"]
            })
        
        return details
    
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
            root (list): A list of roots to query. root is insured to be exist in the word repository in previous process
        
        Returns:
            added(list): A list of serials that are added
            not_added(list): A list of serials that are not added
        """
        added = []
        not_added = []
        for r in roots:
            if r in self.details_youdao["root"].values:
                added.append(r)
            else:
                not_added.append(r)
        return added, not_added
            