import pandas as pd
import os
import random
from models import detail_repo_form

class DetailRepositoryManager:
    def __init__(self):
        self.detail_repo_path = "./assets/detail_repository.csv"
