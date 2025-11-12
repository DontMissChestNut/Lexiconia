from .card_details_manager import CardDetailsManager
from .flashcard_system import FlashcardSystem
from .word_repository_manager import WordRepositoryManager
from .word_to_review_manager import WordToReviewManager 


__all__ = [
    "CardDetailsManager",
    "FlashcardSystem",
    "WordRepositoryManager",
    "WordToReviewManager",
]

card_details_manager = CardDetailsManager()
