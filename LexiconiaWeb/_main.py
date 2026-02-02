from multiprocessing.managers import BaseManager
from operator import ne
import pandas as pd
from datetime import datetime, timedelta, time
from models import CardDetailsManager, WordRepositoryManager, MyReviewManager, Crawler, PathGraphManager, DetailRepositoryManager
from services import LexiconiaService

def main():
    lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, path_graph_manager, detail_repo_manager, updateTime = init()

    words = word_repo_manager.generate_word_list()

    items = []
    item = {
        "root": "string",           # 单词序号 - 00000000
        "serial": "string",         # 详情序号 - 等级-词性-释义-词组
        "sentence": "string",       # 例句序号 - 00000000，例句才会有，否则为0
        "content" : "string",       # 内容
        "translation": "string",    # 翻译/解释
        "synonym": "string",        # 近义词（对称），详情序号（Serial），以;分割
        "antonym": "string",        # 反义词（对称），详情序号（Serial），以;分割
    }
    for word in words:
        items.append({
            "root": "{:0>8d}".format(list(word.keys())[0]),
            "serial": "{:0>2d}{:0>2d}{:0>2d}{:0>2d}".format(0,0,0,0),
            "sentence": "{:0>8d}".format(0),
            "content" : list(word.values())[0],
            "translation": "",   
            "synonym": "",       
            "antonym": "",
        })

    write_csv(items, detail_repo_manager.detail_repo_path, item)

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

if __name__ == "__main__":
    main()
    
    
    



    
