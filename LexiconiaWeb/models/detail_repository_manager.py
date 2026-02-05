import pandas as pd
import os
import random
from models import detail_repo_form, CardDetailsManager

LEVEL_REMAP_N2S = {
    "0": "--",
    "1": "A1",
    "2": "A2",
    "3": "B1",
    "4": "B2",
    "5": "C1",
    "6": "C2",
}

LEVEL_REMAP_S2N = {
    "--": "0",
    "A1": "1",
    "A2": "2",
    "B1": "3",
    "B2": "4",
    "C1": "5",
    "C2": "6",
}

PART_OF_SPEECH_REMAP_N2S = {
    "00": "--",
    "10": "n.",
    "11": "cn.",
    "12": "un.",
    "13": "pn.",
    "20": "v.",
    "21": "vt.",
    "22": "vi.",
    "30": "adj.",
    "40": "adv.",
    "50": "prep.",
    "60": "conj.",
    "70": "exclam.",
    "80": "art.",
    "90": "quant.",
}

PART_OF_SPEECH_REMAP_S2N = {
    "--": "00",
    "n.": "10",
    "cn.": "11",
    "un.": "12",
    "pn.": "13",
    "v.": "20",
    "vt.": "21",
    "vi.": "22",
    "adj.": "30",
    "adv.": "40",
    "prep.": "50",
    "conj.": "60",
    "exclam.": "70",
    "art.": "80",
    "quant.": "90",
}



class DetailRepositoryManager:
    def __init__(self):
        self.detail_repo_path = "./Assets/detail_repository.csv"
        # self.detail_repo = pd.read_csv(self.detail_repo_path, dtype=detail_repo_form)
        self.card_details_manager = CardDetailsManager()
        self._explain_counter = {}

    def generate_line(self, detail:dict):
        root_raw = detail.get("root", 0)
        word = detail.get("word", "")
        level_str = detail.get("level", "--")
        pos_str = detail.get("part of speech", detail.get("part_of_speech", "--"))
        addition = detail.get("addition", "-")
        explaination = detail.get("explaination", "")

        try:
            root_code = "{:0>8d}".format(int(str(root_raw)))
        except:
            root_code = "{:0>8s}".format(str(root_raw)[:8])

        level_second = LEVEL_REMAP_S2N.get(level_str, str(level_str))
        if level_second not in ["0","1","2","3","4","5","6"]:
            level_second = "0"
        level_code = "1" + level_second

        pos_code = PART_OF_SPEECH_REMAP_S2N.get(pos_str, "00")

        counter_key = (str(root_raw), pos_code)
        current = self._explain_counter.get(counter_key, 0) + 1
        self._explain_counter[counter_key] = current
        explain_code = "{:0>2d}".format(current)

        phrase_code = "00"
        serial_code = f"{level_code}{pos_code}{explain_code}{phrase_code}"

        content = word if addition == "-" or addition == "" else f"{word}({addition})"

        line = {
            "root": root_code,
            "serial": serial_code,
            "sentence": "00000000",
            "content": content,
            "translation": explaination,
            "synonym": "",
            "antonym": "",
        }
        return line


class RecordingManager:
    def __init__(self):
        self.recording_path = "g:\\DontMissChestNut\\Lexiconia\\Assets\\review_files\\recording.csv"
        self.output_dir = "./Assets/output"
        # 确保输出目录存在
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # 确保 recording.csv 文件存在 count 列
        self._ensure_count_column()
    
    def _ensure_count_column(self):
        """确保 recording.csv 文件存在 count 列"""
        if not os.path.exists(self.recording_path):
            return
        
        df = pd.read_csv(self.recording_path, encoding="utf-8")
        if "count" not in df.columns:
            df["count"] = 0
            df.to_csv(self.recording_path, index=False, encoding="utf-8")
    
    def read_recording(self):
        """读取 recording.csv 文件"""
        if not os.path.exists(self.recording_path):
            return pd.DataFrame()
        return pd.read_csv(self.recording_path, encoding="utf-8")
    
    def update_count(self, index):
        """更新指定行的 count 列"""
        df = self.read_recording()
        if df.empty or index >= len(df):
            return
        
        df.loc[index, "count"] = df.loc[index, "count"] + 1
        df.to_csv(self.recording_path, index=False, encoding="utf-8")
    
    def get_review_items(self, category, limit=20):
        """按照分类和 count 优先级获取复习项"""
        df = self.read_recording()
        if df.empty:
            return []
        
        # 过滤出指定分类的行
        if "category" in df.columns:
            category_df = df[df["category"].astype(str) == category]
        else:
            # 如果没有 category 列，返回空列表
            return []
        if category_df.empty:
            return []
        
        # 按照 count 升序排序，count 越小优先级越高
        sorted_df = category_df.sort_values(by="count", ascending=True)
        
        # 限制数量
        selected_df = sorted_df.head(limit)
        
        # 转换为列表
        items = []
        for idx, row in selected_df.iterrows():
            items.append({
                "index": idx,
                "root": row.get("root", ""),
                "content": row.get("content", ""),
                "translation": row.get("translation", ""),
                "count": row.get("count", 0)
            })
        
        return items
    
    def generate_review_lists(self):
        """生成复习列表文件"""
        categories = ["错词", "生词", "同义替换", "词伙", "表达优化", "句式", "长句复写", "专有名词"]
        content_file_path = os.path.join(self.output_dir, "review_content.txt")
        answer_file_path = os.path.join(self.output_dir, "review_answer.txt")
        
        # 清空文件
        with open(content_file_path, "w", encoding="utf-8") as f:
            f.write("")
        with open(answer_file_path, "w", encoding="utf-8") as f:
            f.write("")
        
        for category in categories:
            # 获取该分类的复习项
            items = self.get_review_items(category, 20)
            
            # 写入 content 文件
            with open(content_file_path, "a", encoding="utf-8") as f:
                f.write(f"{category}\n")
                for i, item in enumerate(items, 1):
                    f.write(f"({i}) {item.get('translation', '')}\n")
                    f.write(f"(2) xxx\n")
            
            # 写入 answer 文件
            with open(answer_file_path, "a", encoding="utf-8") as f:
                f.write(f"{category}\n")
                for i, item in enumerate(items, 1):
                    f.write(f"({i}) {item.get('content', '')}\n")
                    f.write(f"(2) xxx\n")
            
            # 更新 count
            for item in items:
                self.update_count(item.get('index', 0))
