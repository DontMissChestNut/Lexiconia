from models import CardDetailsManager, FlashcardSystem, WordRepositoryManager, MyReviewManager, Crawler
from services import FlashcardService

if __name__ == "__main__":
    crawler = Crawler()

    word_list = ['yield', 'apace', 'periodical', 'periodically', 'commonwealth', 'dismantle', 'optional', 'attendance', 'inspiring', 'invasion', 'eternal', 'momentary', 'eternity', 'infinite', 'ventilation', 'ventilate', 'counteract', 'forfeit', 'impart', 'companion', 'mutual', 'equity', 'immigration', 'subliminal', 'liminal', 'subliminally', 'consortium', 'hierarchy', 'burgeon', 'regent', 'elicit', 'delve', 'questionnaire', 'questionary', 'substantial', 'substantially', 'sponsor', 'opponent', 'component', 'deliberate', 'ponder']
    roots = [7929, 3090, 2272, 5458, 7031]
    crawler.crawl(roots)
