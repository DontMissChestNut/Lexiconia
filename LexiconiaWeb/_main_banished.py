from multiprocessing.managers import BaseManager
from operator import ne
import pandas as pd
from datetime import datetime, timedelta, time
from models import CardDetailsManager, WordRepositoryManager, MyReviewManager, Crawler, PathGraphManager
from services import LexiconiaService

word_repository_form = {
    "Num": "string",
    "serial" : "string",
    "WordB": "string",
    "WordA": "string",
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

word_to_review_form = {
    "root": "-",
    "Word": "-",
    "CurNode": -1,
    "CurTime": "YYYY-MM-DD-hh-mm-ss",
    "NextTime": "YYYY-MM-DD-hh-mm-ss"
}

path_graph_form = {
    "node": "{:0>6d}".format(0),      # 当前单词节点
    "root": "{:0>6d}".format(0),      # 根词（step=-1），每个单词只有一个根词
    "step0": "string",                # 同根词（对称），存储为JSON数组
    "step1": "string",                # 同根不同义（非对称），存储为JSON数组
    "step2": "string",                # 近义词（对称），存储为JSON数组
    "step3": "string",                # 反义词（对称），存储为JSON数组
    "step4": "string",                # 形近词/音近词（对称），存储为JSON数组
}

card_details_youdao_csv_address = "LexiconiaApp/data/card_details_youdao.csv"

def main():
    lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, path_graph_manager, updateTime = init()

    graph_path = "./Assets/path_graph.csv"
    repository_path = "./Assets/word_repository.csv"

    # graph_df = pd.read_csv(graph_path)
    repository_df = pd.read_csv(repository_path)

    init_graph = []
    for _, row in repository_df.iterrows():
        init_graph.append({
            "node": "{:0>6d}".format(int(row["Num"])),
            "root": "{:0>6d}".format(0),
            "step0": [],
            "step1": [],                
            "step2": [],                
            "step3": [],               
            "step4": [],
        })



def init():
    lexiconia_service  = LexiconiaService()
    word_repo_manager = WordRepositoryManager()
    detail_manager = CardDetailsManager()
    my_review_manager = MyReviewManager()
    path_graph_manager = PathGraphManager()
    crawler = Crawler()

    updateTime = time(5, 0, 0)  # 05:00:00

    return lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, path_graph_manager, updateTime

def write_csv(data, path, form):
    df = pd.DataFrame(columns = form.keys())
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=False)
    df.to_csv(path, index=False, encoding="utf-8")

if __name__ == "__main__":
    main()
    
    
    



    
