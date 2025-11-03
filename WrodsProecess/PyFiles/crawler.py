# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup           # 网页解析，获取数据
import re                               # 正则表达式，进行文字匹配`
import urllib.request, urllib.error     # 制定URL，获取网页数据
# import xlwt                             # 进行excel操作
# import sqlite3                         # 进行SQLite数据库操作

class Crawler:
    def __init__(self):
        # 初始化网页及文件位置
        self.base_url = "https://oalecd10.cp.com.cn"
        self.search_api = "https://oalecd10.cp.com.cn/entry/api/search"  # 需要确认实际API

        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://oalecd10.cp.com.cn/",
            "Accept": "application/json, text/plain, */*"
        }
        
        
        # 测试信息
        self.word_list = ['yield', 'apace', 'periodical', 'periodically', 'commonwealth', 'dismantle', 'optional', 'attendance', 'inspiring', 'invasion', 'eternal', 'momentary', 'eternity', 'infinite', 'ventilation', 'ventilate', 'counteract', 'forfeit', 'impart', 'companion', 'mutual', 'equity', 'immigration', 'subliminal', 'liminal', 'subliminally', 'consortium', 'hierarchy', 'burgeon', 'regent', 'elicit', 'delve', 'questionnaire', 'questionary', 'substantial', 'substantially', 'sponsor', 'opponent', 'component', 'deliberate', 'ponder']
        
    def crawl(self, url, save_path):
        """Main crawl mathod

        Args:
            save_path (string): save information
        """
        
        print("开始查询单词")
        data_list = self._get_data(url, self.word_list)
        
        print("保存爬取数据")
        self._save_data(data_list, save_path)
        
        print(f"爬取完成！数据已保存至: {save_path}")
        return data_list
        
    def _get_data(self, base_url, word_list):

        data_list = []
        
        for word in word_list:
            
            pass
        
        