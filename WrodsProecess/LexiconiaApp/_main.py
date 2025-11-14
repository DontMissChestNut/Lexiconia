from models import CardDetailsManager, FlashcardSystem, WordRepositoryManager, MyReviewManager
from services import FlashcardService

if __name__ == "__main__":
    flashcard_service = FlashcardService()
    print(1)
    print(flashcard_service.type)
    flashcard_service.add_my_review(["a","b","c","apple"])
