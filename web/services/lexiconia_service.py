import pandas as pd
from models import WordRepositoryManager, PathGraphManager

class LexiconiaService:
    """单词卡业务逻辑服务"""
    
    def __init__(self):
        self.word_repo = WordRepositoryManager()
        self.path_graph = PathGraphManager()