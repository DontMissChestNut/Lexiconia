from operator import ne
import pandas as pd
from datetime import datetime, timedelta, time
from models import CardDetailsManager, WordRepositoryManager, MyReviewManager, Crawler
from services import LexiconiaService

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

card_details_youdao_csv_address = "LexiconiaApp/data/card_details_youdao.csv"

def main():
    lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, updateTime = init()
    
    root = [3561, 7530, 4811, 3054, 1103, 3377, 7889, 8213, 1046, 7125, 7381, 7386, 8347, 3966]
    # lexiconia_service .update_view_status_nodes(root)
    
    print(lexiconia_service .update_view_status_nodes(root))


def init():
    lexiconia_service  = LexiconiaService()
    word_repo_manager = WordRepositoryManager()
    detail_manager = CardDetailsManager()
    my_review_manager = MyReviewManager()
    crawler = Crawler()

    updateTime = time(5, 0, 0)  # 05:00:00

    return lexiconia_service , word_repo_manager, detail_manager, my_review_manager, crawler, updateTime

if __name__ == "__main__":
    main()
    
    
    



    
