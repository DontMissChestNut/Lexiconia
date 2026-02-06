import pandas as pd
from models import word_repository_form

"""
WordRepositoryManager
"""

word_repository_form = {
    "num": "string",            # "{:0>8d}".format(list(word.keys())[0]),    
    "word_b": "string",
    "word_a": "string",

}

class WordRepositoryManager:
    def __init__(self):
        self.file_path = "./Assets/word_repository.csv"

    def get_words_by_root(self, root: str) -> str:
        return "-"
    
    def get_words_by_roots(self, roots: list) -> list:
        return []
    