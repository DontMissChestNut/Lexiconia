import pandas as pd

word_card_form= {
    "Root": "string",
    "Serial" : "string",
    "Level": "string",
    "part_of_speech": "string",
    "Addition": "string",           # 名词复数、动词变形等
    "ExplainationE": "string",
    "ExplainationC": "string",
    # "Phonetic": "string"          # TODO： 音标
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
            