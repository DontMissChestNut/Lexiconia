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
        """Main crawl method"""

        words = self.word_repo.get_words_by_roots(roots)
        for word in words:
            root, word = word
            url = self.search_api.format(word)
            response = requests.get(url, headers=self.headers)

            detail = self._parse_and_save_word_info(root, response.content.decode(response.apparent_encoding))
            

        # url = self.search_api.format("yield")
        # response = requests.get(self.search_api.format("yield"))
        
        # # 保存原始HTML到文件
        # with open("tieba.txt", "w", encoding=response.apparent_encoding) as f:
        #     f.write(response.content.decode(response.apparent_encoding))
        
        # print("原始网页已保存到 tieba.txt")
        
        # 直接解析响应内容并提取单词信息
        # details = self._parse_and_save_word_info(roots, response.content.decode(response.apparent_encoding))

        # print(details)
        
    def _parse_and_save_word_info(self, root, html_content):
        """解析HTML并保存单词信息到文件"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找class="simple dict-module"的div
        simple_dict_module = soup.find('div', class_='simple dict-module')
        
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
                    addition = self.switch_wfs(addition, wfs_text)
                    # addition += f"{wfs_text}: {trans_text};"
                    # print("addition:", addition)
            # for i in range(len(details)):
            #     details[i]["Addition"] = addition

        # if simple_dict_module:
        #     # 在该div内查找所有class="word-exp"的标签
        #     word_exps = simple_dict_module.find_all('li', class_='word-exp')          
            
        #     details = []
        #     for i, word_exp in enumerate(word_exps, 1):
        #         # 提取词性和释义
        #         pos = word_exp.find('span', class_='pos')
        #         trans = word_exp.find('span', class_='trans')
                
        #         pos_text = pos.get_text(strip=True) if pos else "未知词性"
        #         trans_text = trans.get_text(strip=True) if trans else "无释义"
                
        #         detail = {
        #             "Root": root,
        #             "Serial": "19-{:0>6d}-00-0".format(int(root)),
        #             "Level": "9",
        #             "part_of_speech": pos_text,
        #             "Addition": "-",
        #             "ExplainationE": trans_text,
        #             "ExplainationC": "-",
        #         }
            

        # else:
        #     output_lines.append("未找到class='simple dict-module'的标签")
        
        # return details
        
    def http(self, url):
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/"}
        response = requests.get(url, headers=headers)
        return response.content.decode(response.apparent_encoding)
        
    def http(self, url):
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/"}
        response = requests.get(url,headers=headers)
        return response.content.decode(response.apparent_encoding)
    
    def switch_wfs(self, addition:dict, wfs_text:str):
        match wfs_text:
            case "复数":
                addition["things"] = wfs_text
            case "第三人称单数":
                addition["does"] = wfs_text
            case "现在分词":
                addition["doing"] = wfs_text
            case "过去式":
                addition["did"] = wfs_text
            case "过去分词":
                addition["done"] = wfs_text
            case "比较级":
                addition["better"] = wfs_text
            case "最高级":
                addition["best"] = wfs_text
        return addition
