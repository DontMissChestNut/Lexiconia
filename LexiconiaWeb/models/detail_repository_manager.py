import pandas as pd
from models import detail_repo_form


class DetailRepositoryManager:
    def __init__(self):
        self.detail_repo_path = "./Assets/detail_repository.csv"
        # self.detail_repo = pd.read_csv(self.detail_repo_path, dtype=detail_repo_form)