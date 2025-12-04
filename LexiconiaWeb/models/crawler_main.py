# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup           # 网页解析，获取数据
import re                               # 正则表达式，进行文字匹配`
import urllib.request, urllib.error     # 制定URL，获取网页数据
# import xlwt                             # 进行excel操作
# import sqlite3                         # 进行SQLite数据库操作
import requests                         # 网页解析，获取数据
from lxml import etree

from models import WordRepositoryManager

word_card_form_youdao= {
    "Root": "string",
    "Serial" : "10-000000-00-0",        # youdao(1)+level - root - part of speech - num
    "Level": "string",
    "part_of_speech": "string",
    "Addition": "string",           # 名词复数、动词变形等
    "ExplainationE": "string",
    "ExplainationC": "string",
    # "Phonetic": "string"          # TODO： 音标
}
 
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"

 
url = "https://www.shicimingjv.com/bookview/1392.html"

class Crawler:
    def __init__(self):
        # 初始化网页及文件位置
        self.base_url = "https://dict.youdao.com"
        self.search_api = "https://dict.youdao.com/result?word={}&lang=en"  # 需要确认实际API

        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://oalecd10.cp.com.cn/",
            "Accept": "application/json, text/plain, */*"
        }

        self.word_repo = WordRepositoryManager()
        
    def crawl(self, roots: list):
        """
        Main crawl method
        
        Args:
            roots (list): A list of roots to crawl. Root is insured to be exist in the word repository in previous process
        """

        words = self.word_repo.get_words_by_roots(roots)
        details = []
        for word in words:
            root, word = word
            url = self.search_api.format(word)
            response = requests.get(url, headers=self.headers)

            # detail = self._parse_and_save_word_info(root, response.content.decode(response.apparent_encoding))
            details.append(self._parse_and_save_word_info(root, response.content.decode(response.apparent_encoding)))            

        return details
        
    def _parse_and_save_word_info(self, root, html_content):
        """解析HTML并保存单词信息到文件"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找class="simple dict-module"的div
        simple_dict_module = soup.find('div', class_='simple dict-module')

        if not simple_dict_module:
            return None
        
        # 先提取单词变形信息
        addition ={
            "things": "",
            "does": "",
            "doing": "",
            "did": "",
            "done": "",
            "better": "",
            "best": "",
        }
        word_forms = simple_dict_module.find_all('li', class_='word-wfs-cell-less')
        if word_forms:

            for form in word_forms:
                wfs_name = form.find('span', class_='wfs-name')
                transformation = form.find('span', class_='transformation')
                
                wfs_text = wfs_name.get_text(strip=True) if wfs_name else ""
                trans_text = transformation.get_text(strip=True) if transformation else ""
                
                if wfs_text and trans_text:
                    addition = self._switch_wfs(addition, wfs_text, trans_text)
        
        if simple_dict_module:
            # 在该div内查找所有class="word-exp"的标签
            word_exps = simple_dict_module.find_all('li', class_='word-exp')          
            
            details = []
            for i, word_exp in enumerate(word_exps, 1):
                # 提取词性和释义
                pos = word_exp.find('span', class_='pos')
                trans = word_exp.find('span', class_='trans')
                
                pos_text = pos.get_text(strip=True) if pos else "-"
                trans_text = trans.get_text(strip=True) if trans else "-"
                
                details.append({
                    "Root": "{:0>6d}".format(int(root)),
                    "Serial": "19-{:0>6d}-00-{}".format(int(root), i),
                    "Level": "9",
                    "part_of_speech": pos_text,
                    "Addition": self._switch_pfs(pos_text, addition),
                    "ExplainationE": "-",
                    "ExplainationC": trans_text,
                })

        return details      
        
    def http(self, url):
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/"}
        response = requests.get(url, headers=headers)
        return response.content.decode(response.apparent_encoding)
        
    def http(self, url):
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/"}
        response = requests.get(url,headers=headers)
        return response.content.decode(response.apparent_encoding)
    
    def _switch_wfs(self, addition:dict, wfs_text:str, trans_text:str):
        match wfs_text:
            case "复数":
                addition["things"] = trans_text
            case "第三人称单数":
                addition["does"] = trans_text
            case "现在分词":
                addition["doing"] = trans_text
            case "过去式":
                addition["did"] = trans_text
            case "过去分词":
                addition["done"] = trans_text
            case "比较级":
                addition["better"] = trans_text
            case "最高级":
                addition["best"] = trans_text
        return addition
    
    def _switch_pfs(self, pfs_text:str, addition:dict):
        add = "-"
        match pfs_text:
            case "n.":
                add = addition["things"]
            case "v.":
                add = "{}-{}-{}-{}".format(addition["does"], addition["doing"], addition["did"], addition["done"])
            case "adj.":
                add = "{}-{}".format(addition["better"], addition["best"])
        
        if len([_ for _ in add.split("-") if _ != ""]) == 0:
            add = "-"
        
        return add
        
        
