from multiprocessing.managers import BaseManager
from operator import ne
import pandas as pd
from datetime import datetime, timedelta, time
import os
from models import CardDetailsManager, WordRepositoryManager, MyReviewManager, Crawler, PathGraphManager, DetailRepositoryManager
from models import detail_repo_form
from services import LexiconiaService

def main():
    lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, path_graph_manager, detail_repo_manager, updateTime = init()

    youdao_detail_path = detail_manager.file_youdao_path
    detai_repo = pd.read_csv(youdao_detail_path, dtype=detail_repo_form)
    
    words = word_repo_manager.generate_word_list()

    clips = []
    for _ in words:
        num = list(_.keys())[0]
        word = list(_.values())[0]
        
        clips.append((num, word))
    

    txt_path = os.path.join(os.path.dirname(__file__), "clips.txt")
    write_txt(clips, txt_path)
    loaded_clips = read_txt(txt_path, 200)

    print(loaded_clips)

    details = []
    for _ in loaded_clips:
        d = crawler.crawl_byword(_[1])
        if d:
            for __ in d:
                details.append({
                    "root": int(_[0]),
                    "word": _[1],
                    "level" : detail_manager.get_level_by_root(int(_[0])),
                    "part of speech": __["part of speech"],
                    "addition": __["addition"],
                    "explaination": __["explaination"],
                })
    
    lines = []
    for _ in details:
        lines.append(detail_repo_manager.generate_line(_))
      
    write_csv_append(detail_repo_manager.detail_repo_path, lines, detail_repo_form)
    
    

def init():
    lexiconia_service  = LexiconiaService()
    word_repo_manager = WordRepositoryManager()
    detail_manager = CardDetailsManager()
    my_review_manager = MyReviewManager()
    path_graph_manager = PathGraphManager()
    detail_repo_manager = DetailRepositoryManager()
    crawler = Crawler()

    updateTime = time(5, 0, 0)  # 05:00:00

    return lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, path_graph_manager, detail_repo_manager, updateTime

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

if __name__ == "__main__":
    main()
    
    
    



    
