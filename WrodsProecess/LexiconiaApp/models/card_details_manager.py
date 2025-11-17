import pandas as pd

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
        
        self.details = pd.read_csv(self.detail_path)
        pass

    def add_card_detail(self, card_detail: dict):
        """添加卡片详情"""
        cardf = pd.DataFrame([card_detail], columns=word_card_form.keys())
        cardf.to_csv(self.detail_path, mode="a", index=False, header=False, encoding="utf-8")
        return

    def erase_card_detail(self, serial: str):
        """删除卡片详情"""
        df = pd.read_csv(self.detail_path, encoding="utf-8", header=0)
        df = df[df["Serial"] != serial]
        df.to_csv(self.detail_path, mode="w", index=False, header=True, encoding="utf-8")
        return
    
    def rewrite_card_detail(self, card_detail: dict, serial: str):
        """重写卡片详情"""
        df = pd.read_csv(self.detail_path, encoding="utf-8", header=0)
        df = df[df["Serial"] != serial]
        df.to_csv(self.detail_path, mode="w", index=False, header=True, encoding="utf-8")
        self.add_card_detail(card_detail)
        return

    def rewrite_card_detail_youdao(self, card_detail: dict, serial: str):
        """重写卡片详情"""
        
        return
    
    def get_details_by_root(self, root:int):
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
            