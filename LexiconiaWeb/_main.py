from multiprocessing.managers import BaseManager
from operator import ne
import pandas as pd
from datetime import datetime, timedelta, time
import os
from models import CardDetailsManager, WordRepositoryManager, MyReviewManager, Crawler, PathGraphManager, DetailRepositoryManager, RecordingManager
from models import detail_repo_form
from services import LexiconiaService

def main():
    lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, path_graph_manager, detail_repo_manager, recording_manager, updateTime = init()
    # daily_path = "./Assets/review_files/daily_words.txt"
    # detail_path = "./Assets/detail_repository copy.csv"
    # word_repo_path = "./Assets/word_repository.csv"
    # merge_word_repository(daily_path, detail_path, word_repo_path)
    
    # 处理 recording.csv 文件
    recording_path = "g:\\DontMissChestNut\\Lexiconia\\Assets\\review_files\\recording.csv"
    word_repo_path = "g:\\DontMissChestNut\\Lexiconia\\Assets\\word_repository.csv"
    merge_recording_to_word_repo(recording_path, word_repo_path)
    
    # 生成复习列表
    recording_manager.generate_review_lists()


def init():
    lexiconia_service  = LexiconiaService()
    word_repo_manager = WordRepositoryManager()
    detail_manager = CardDetailsManager()
    my_review_manager = MyReviewManager()
    path_graph_manager = PathGraphManager()
    detail_repo_manager = DetailRepositoryManager()
    recording_manager = RecordingManager()
    crawler = Crawler()

    updateTime = time(5, 0, 0)  # 05:00:00

    return lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, path_graph_manager, detail_repo_manager, recording_manager, updateTime

def write_csv(data, path, form):
    df = pd.DataFrame(columns = form.keys())
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=False)
    df.to_csv(path, index=False, encoding="utf-8")

def write_csv_append(path, data, form):
    columns = list(form.keys())
    df = pd.DataFrame(data, columns=columns)
    header = (not os.path.exists(path)) or (os.path.getsize(path) == 0)
    df.to_csv(path, mode="a", header=header, index=False, encoding="utf-8")

def write_txt(clips, path):
    with open(path, "w", encoding="utf-8") as f:
        for num, word in clips:
            f.write(f"{num}\t{word}\n")

def read_txt(path, end, chunk=100):
    start = max(0, end - chunk)
    result = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx < start:
                continue
            if idx >= end:
                break
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                result.append((parts[0], parts[1]))
    return result

def parse_daily_words(path):
    result = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            for token in line.split(","):
                w = token.strip().replace("*", "")
                if w:
                    result.add(w)
    return list(result)

def read_detail_repo(path):
    df = pd.read_csv(path, encoding="utf-8")
    if "root" not in df.columns or "content" not in df.columns:
        return []
    df = df[["root", "content"]].dropna()
    rows = []
    for _, r in df.iterrows():
        root = str(r["root"]).strip()
        content = str(r["content"]).strip()
        if root and content:
            rows.append((root, content))
    return rows

def read_word_repository(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pd.DataFrame(columns=["num", "word_b", "word_a"])
    df = pd.read_csv(path, encoding="utf-8")
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(columns={"num": "num", "wordb": "word_b", "worda": "word_a"})
    df = df.loc[:, ~pd.Index(df.columns).duplicated()]
    cols = ["num", "word_b", "word_a"]
    for c in cols:
        if c not in df.columns:
            df[c] = pd.Series(dtype=str)
    return df[cols]

def read_recording(path):
    df = pd.read_csv(path, encoding="utf-8")
    if "root" not in df.columns:
        return []
    df = df[["root"]].dropna()
    roots = []
    for _, r in df.iterrows():
        root = str(r["root"]).strip()
        if root:
            roots.append(root)
    return roots

def write_word_repository_append(path, rows):
    cols = ["num", "word_b", "word_a"]
    df = pd.DataFrame(rows, columns=cols)
    header = (not os.path.exists(path)) or (os.path.getsize(path) == 0)
    df.to_csv(path, mode="a", header=header, index=False, encoding="utf-8")

def merge_word_repository(daily_path, detail_path, word_repo_path):
    existing = read_word_repository(word_repo_path)
    existing_words = set([str(x).strip() for x in existing["word_b"].tolist()]) if not existing.empty else set()
    detail_rows = read_detail_repo(detail_path)
    seen_detail = set()
    to_write = []
    max_root = 0
    for root, word in detail_rows:
        try:
            n = int(str(root))
            if n > max_root:
                max_root = n
        except:
            pass
        w = word
        if w in existing_words or w in seen_detail:
            continue
        try:
            num_str = "{:0>8d}".format(int(str(root)))
        except:
            num_str = "{:0>8d}".format(max_root)
        to_write.append([num_str, w, w])
        seen_detail.add(w)
    daily_words = parse_daily_words(daily_path)
    current = max_root
    for w in daily_words:
        if w in existing_words or w in seen_detail:
            continue
        current += 1
        num_str = "{:0>8d}".format(current)
        to_write.append([num_str, w, w])
    if to_write:
        write_word_repository_append(word_repo_path, to_write)

def merge_recording_to_word_repo(recording_path, word_repo_path):
    existing = read_word_repository(word_repo_path)
    existing_words = set([str(x).strip() for x in existing["word_b"].tolist()]) if not existing.empty else set()
    recording_roots = read_recording(recording_path)
    seen_roots = set()
    to_write = []
    # 计算当前最大 num 值
    current_num = 0
    if not existing.empty:
        for num in existing["num"]:
            try:
                n = int(str(num))
                if n > current_num:
                    current_num = n
            except:
                pass
    # 处理 recording 中的 root
    for root in recording_roots:
        root_stripped = str(root).strip()
        if not root_stripped or root_stripped in existing_words or root_stripped in seen_roots:
            continue
        current_num += 1
        num_str = "{:0>8d}".format(current_num)
        to_write.append([num_str, root_stripped, root_stripped])
        seen_roots.add(root_stripped)
    if to_write:
        write_word_repository_append(word_repo_path, to_write)

if __name__ == "__main__":
    main()
    
    
    



    
