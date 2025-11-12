import pandas as pd

word_card_form= {
    "Root": "string",
    "Serial" : "string",
    "Level": "string",
    "Part of Speech": "string",
    "addition": "string",
    "ExplainationE": "string",
    "ExplainationC": "string"
}

class CardDetailsManager:
    def __init__(self):
        self.detail_path = "LexiconiaApp/data/card_details.csv"
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