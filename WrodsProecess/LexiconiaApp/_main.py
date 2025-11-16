from models import CardDetailsManager, FlashcardSystem, WordRepositoryManager, MyReviewManager
from services import FlashcardService

if __name__ == "__main__":
    flashcard_service = FlashcardService()

    roots = [7929, 3090, 2272, 5458, 7031]
    flashcard_service.update_view_status_nodes(roots, 0)
