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

    word_list = ['yield', 'apace', 'periodical', 'periodically', 'commonwealth', 'dismantle', 'optional', 'attendance', 'inspiring', 'invasion', 'eternal', 'momentary', 'eternity', 'infinite', 'ventilation', 'ventilate', 'counteract', 'forfeit', 'impart', 'companion', 'mutual', 'equity', 'immigration', 'subliminal', 'liminal', 'subliminally', 'consortium', 'hierarchy', 'burgeon', 'regent', 'elicit', 'delve', 'questionnaire', 'questionary', 'substantial', 'substantially', 'sponsor', 'opponent', 'component', 'deliberate', 'ponder']

    word_list = flashcard_service.prepare_my_review(10, "youdao")

    # roots = [i["Root"] for i in word_list]

    # print(detail_manager.update_youdao_details(roots))


def init():
    flashcard_service = FlashcardService()
    word_repo_manager = WordRepositoryManager()
    detail_manager = CardDetailsManager()
    my_review_manager = MyReviewManager()
    crawler = Crawler()

    return flashcard_service, word_repo_manager, detail_manager, my_review_manager, crawler

if __name__ == "__main__":
    main()
    
    
    



    
