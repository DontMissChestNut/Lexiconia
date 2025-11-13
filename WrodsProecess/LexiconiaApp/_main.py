from models import CardDetailsManager, FlashcardSystem, WordRepositoryManager, MyReviewManager

if __name__ == "__main__":
    my_review_manager = MyReviewManager()
    my_review_manager.new_word("hello")