# -*- coding: utf-8 -*-
import re
import urllib.request
import urllib.error
import xlwt
from bs4 import BeautifulSoup


class DoubanMovieCrawler:
    """豆瓣电影Top250爬虫类"""
    
    def __init__(self):
        # 初始化正则表达式模式
        self.findLink = re.compile(r'<a href="(.*?)">')
        self.findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
        self.findTitle = re.compile(r'<span class="title">(.*)</span>')
        self.findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
        self.findJudge = re.compile(r'<span>(\d*)人评价</span>')
        self.findInq = re.compile(r'<span class="inq">(.*)</span>')
        self.findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
        
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
        }
    
    def crawl(self, save_path="豆瓣电影Top250.xls"):
        """主爬取方法"""
        base_url = "https://movie.douban.com/top250?start="
        
        print("开始爬取豆瓣电影Top250...")
        data_list = self._get_data(base_url)
        
        print("正在保存数据...")
        self._save_data(data_list, save_path)
        
        print(f"爬取完成！数据已保存至: {save_path}")
        return data_list
    
    def _get_data(self, base_url):
        """获取所有电影数据"""
        data_list = []
        
        for i in range(0, 10):  # 爬取10页
            print(f"正在爬取第{i+1}页...")
            url = base_url + str(i * 25)
            html = self._ask_url(url)
            
            if html:
                soup = BeautifulSoup(html, "html.parser")
                page_data = self._parse_page(soup)
                data_list.extend(page_data)
        
        return data_list
    
    def _parse_page(self, soup):
        """解析单页数据"""
        page_data = []
        
        for item in soup.find_all('div', class_="item"):
            data = []
            item_str = str(item)
            
            # 提取各项信息
            link = self._extract_link(item_str)
            img_src = self._extract_img_src(item_str)
            titles = self._extract_titles(item_str)
            rating = self._extract_rating(item_str)
            judge_num = self._extract_judge_num(item_str)
            inq = self._extract_inq(item_str)
            bd = self._extract_bd(item_str)
            
            # 组装数据
            data.extend([link, img_src])
            data.extend(titles)
            data.extend([rating, judge_num, inq, bd])
            
            page_data.append(data)
        
        return page_data
    
    def _extract_link(self, item_str):
        """提取电影链接"""
        link = re.findall(self.findLink, item_str)[0]
        return link
    
    def _extract_img_src(self, item_str):
        """提取图片链接"""
        img_src = re.findall(self.findImgSrc, item_str)[0]
        return img_src
    
    def _extract_titles(self, item_str):
        """提取电影标题（中文和英文）"""
        titles = re.findall(self.findTitle, item_str)
        if len(titles) == 2:
            ctitle = titles[0]
            otitle = titles[1].replace("/", "")
        else:
            ctitle = titles[0]
            otitle = " "
        return [ctitle, otitle]
    
    def _extract_rating(self, item_str):
        """提取评分"""
        rating = re.findall(self.findRating, item_str)[0]
        return rating
    
    def _extract_judge_num(self, item_str):
        """提取评价人数"""
        judge_num = re.findall(self.findJudge, item_str)[0]
        return judge_num
    
    def _extract_inq(self, item_str):
        """提取电影简介"""
        inq = re.findall(self.findInq, item_str)
        if len(inq) != 0:
            inq = inq[0].replace("。", "")
        else:
            inq = " "
        return inq
    
    def _extract_bd(self, item_str):
        """提取电影详细信息"""
        bd = re.findall(self.findBd, item_str)[0]
        bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
        bd = re.sub('/', "", bd)
        return bd.strip()
    
    def _ask_url(self, url):
        """请求URL获取网页内容"""
        request = urllib.request.Request(url, headers=self.headers)
        html = ""
        
        try:
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(f"请求错误，错误代码: {e.code}")
            if hasattr(e, "reason"):
                print(f"请求错误，原因: {e.reason}")
        
        return html
    
    def _save_data(self, data_list, save_path):
        """保存数据到Excel文件"""
        book = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
        
        # 设置列名
        columns = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
        for i, col_name in enumerate(columns):
            sheet.write(0, i, col_name)
        
        # 写入数据
        for i, data in enumerate(data_list):
            for j, value in enumerate(data):
                sheet.write(i + 1, j, value)
        
        book.save(save_path)


# 使用示例
if __name__ == "__main__":
    # 创建爬虫实例
    crawler = DoubanMovieCrawler()
    
    # 执行爬取
    crawler.crawl()