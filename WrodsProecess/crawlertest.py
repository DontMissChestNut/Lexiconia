# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup           # 网页解析，获取数据
import re                               # 正则表达式，进行文字匹配`
import urllib.request, urllib.error     # 制定URL，获取网页数据
import xlwt                             # 进行excel操作
import sqlite3                          # 进行SQLite数据库操作

base_url = "https://dict.youdao.com/result?word=lated&lang=en"

text_path = "test.txt"

def main():
    html = askURL(base_url)
    
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(html)

def askURL(url):
    # 模拟浏览器头部信息，向豆瓣服务器发送消息
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    head = {    
         "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    
    request = urllib.request.Request(url, headers=head)
    
    html = ""
    
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            # print(e.code)
        if hasattr(e, "reason"):
            # print(e.reason)
    
    return html

if __name__ == "__main__":
    main()