from operator import ne
import pandas as pd
from models import CardDetailsManager, WordRepositoryManager, MyReviewManager, Crawler
from services import FlashcardService

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
    flashcard_service, word_repo_manager, detail_manager, my_review_manager, crawler = init()

    due_reviews = flashcard_service.get_daily_reviews()

    for review in due_reviews:
        for i in review["Details"]:
            add = [_ for _ in i["Addition"].split("-") if _ != ""]
            print(add, len(add))


def init():
    flashcard_service = FlashcardService()
    word_repo_manager = WordRepositoryManager()
    detail_manager = CardDetailsManager()
    my_review_manager = MyReviewManager()
    crawler = Crawler()

    return flashcard_service, word_repo_manager, detail_manager, my_review_manager, crawler

if __name__ == "__main__":
    main()
    
    
    



    
