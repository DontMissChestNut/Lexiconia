from datetime import date
from pydoc import cram
import copy
from bs4 import BeautifulSoup, Tag
import json
import re

OFXORD_DICT_FORM = {
    "hearder": {
        "word": "str",
        "pronunciation": "str",
        "part_of_speech": "str",
        "symbols": "str",
    },
}

class OxfordDictProcessor:
    def __init__(self):
        self.soup = None

        self.icon_urls = []

        self.header = None
        self.definitions = None

        self.symbol_mapping = {
            "Ox3000 key_L": "Oxford-3000",
            "CET4": "CET4",
            "CET6": "CET6",
            "CEFR_B2_S": "B2",
            "GRE": "GRE",
            "NETM": "NETM",
            "TOEFL": "toefl",
        }

        self.tab_mapping = {
            "n.": "noun",
            "v.": "verb",
            "adj.": "adjective",
            "adv.": "adverb",
        }
        
        # 读取HTML文件
        with open('OxfordDictProcessor/test.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, 'html.parser')
        self.soup = BeautifulSoup(html_content, 'html.parser')

    """提取单词基本信息：单词、音标、词性、等级等
    """
    def extract_word_header(self):
        result = {
            "word": "",
            "pronunciation": "",
            "symbols": [],
        }

        # 提取单词本身
        word_elem = self.soup.find('span', class_='vocabulary-top_main__ibK-6')
        if word_elem:
            result['word'] = word_elem.get_text(strip=True)

        # 提取音标和发音
        pronunciation = {}
        pronunciation_chunks = self.soup.find_all('div', class_='vocabulary-top_chunk__4312R')
        if not pronunciation_chunks:
            pronunciation_chunks = self.soup.find_all('span', class_='vocabulary-top_chunk__4312R')
        
        for chunk in pronunciation_chunks:
            # 提取地区（BrE或NAmE）
            geo_elem = chunk.find('span', class_='vocabulary-top_geo__Pw685')
            
            if geo_elem:
                geo = geo_elem.get_text(strip=True)
                # 提取音标
                phon_elem = chunk.find('b', class_='vocabulary-top_phon__cNeQH')
                if phon_elem:
                    pronunciation[geo] = phon_elem.get_text(strip=True)
        
        result['pronunciation'] = pronunciation

        # 提取单词等级标签（CET4, CET6等）
        symbols = []
        symbol_elems = self.soup.find_all('span', class_='vocabulary-top_symbol__xpmIs')
        for symbol_elem in symbol_elems:
            img_elem = symbol_elem.find('img')
            if img_elem and 'alt' in img_elem.attrs:
                symbols.append(img_elem['alt'])
                if img_elem['src'] not in self.icon_urls:
                    self.icon_urls.append(img_elem['src'])
        result['symbols'] = symbols
        
        self.header = result
        
        return result

    def extract_definitions(self):
        results = []
        result = {
            "part_of_speech": "",
            "definitions": [],
        }

        define = {
            "chunk_group":{
                "eng":  "str",
                "simp": "str",
            },
        }

        # 提取词性标签（noun, verb, adj等）
        tabs = []
        try_tabs = self.soup.find_all('div', class_="tabs_tab__IVkNv")
        for tab in try_tabs:
            tabs.append(self.tab_mapping[tab.get_text(strip=True)])
        # print(tabs)
        
        # 提取每个词性的详细释义
        word_details = self.soup.find_all('div', id="wordDetail")
        for idx, wordDetail in enumerate(word_details):
            rs_detail = []
            """rs_detail[x] = {
                "part_of_speech": tabs[idx],
                "chunks": [],
                "definitions": [],
            }"""
            part_of_speech_elem = tabs[idx]
            detail_section = wordDetail.find_all('div', class_="vocabulary-top_multipleSense__wX134")
            for detail in detail_section:
                chunk_group = detail.find('div', class_="vocabulary-chunk_group__FrAQ9 vocabulary-chunk_inline__uWEOK vocabulary-top_eng__VWJ54")
                explains = detail.find_all('div', class_="vocabulary-top_sense__Fja-g")

                re_chunk_group = []
                if chunk_group:
                    temp = chunk_group.find_all('span', class_="vocabulary-chunk_root__sjfAa vocabulary-chunk_bold__Cb0D1")
                    en = ""
                    simp = ""
                    for i in temp:
                        match i["data-tag"]:
                            case "eng":
                                en += i.get_text(strip=True) + " "
                            case "simp":
                                simp += i.get_text(strip=True)
                    re_chunk_group = [en.replace("  ", " "), simp.strip()]

                re_define = []
                if explains:
                    for explain in explains:
                        # temp = explain.find_all('span', class_="vocabulary-chunk_root__sjfAa")
                        # print(explain)
                        if explain.parent.parent.find("div", id="idiomBlocks"):  
                            basic_explain = explain.find('div', class_="vocabulary-chunk_group__FrAQ9")
                            example_list = explain.find('ul', class_="vocabulary-top_exampleList__j+ZMa")

                            # 提取基本释义
                            rs_basic_explain = []
                            temp = basic_explain.find_all('span')
                            num = temp[0].get_text(strip=True) + temp[1].get_text(strip=True)

                            num = ""
                            en = ""
                            simp = ""
                            for t in temp:
                                if "data-tag" in t.attrs:
                                    if t["data-tag"] == "sn-g":
                                        num += t["data-search-key"]
                                    elif t["data-tag"] == "simp":
                                        simp += t["data-search-key"]
                                    else:
                                        en += t["data-search-key"].replace("\n", "") + " "
                                        
                                elif ("data-tag" not in t.attrs):
                                    print(t.attrs.keys())
                                    if "data-gram-key" in t.attrs:
                                        en += t.get_text(strip=True).replace("\n", "") + " "
                                    else:
                                        num += t.get_text(strip=True)
                                # if t.class_ != "vocabulary-chunk_root__sjfAa":
                                #     continue
                            
                                # if "data-symbol-key" in t.attrs:
                                #     print(t["data-symbol-key"])
                                # elif "data-search-key" in t.attrs:
                                #     print(t["data-search-key"])
                                # elif "data-gram-key" in t.attrs:
                                #     print(t["data-gram-key"])
                                elif "data-tag" in t.attrs and t["data-tag"] == "simp":
                                    simp += t.get_text(strip=True)
                                    
                                else:
                                    en += t.get_text(strip=True).replace("\n", "") + " "
                            
                            rs_basic_explain = [num, en.replace("  ", " "), simp]
                            # print(rs_basic_explain)
                            # print(num)
                        else:
                            print("idiomBlocks")
                    #     temp = explain.find_all('span', class_="vocabulary-chunk_root__sjfAa")
                        
                    #     en = ""
                    #     simp = ""
                    #     for i in temp:
                            
                    #         if isinstance(i, Tag) :
                    #             # print(i["data-tag"])
                    #         #     if i["data-tag"] == "eng":
                    #         #     
                    #             if "data-tag" in i.attrs and i["data-tag"] == "sn-g":
                    #                 continue
                    #             elif "data-tag" in i.attrs and i["data-tag"] == "simp":
                    #                 simp += i.get_text(strip=True)
                    #             elif "data-gram-key" in i.attrs:
                    #                 en += i["data-gram-key"] + " "
                    #             else:
                    #                 en += (i.get_text(strip=True) + " ").replace("\n", "")
                    #     re_define.append([en.replace("  ", " "), simp.strip()])
                    #     # print([en.replace("  ", " "), simp.strip()])
                    # else:
                    #     print("idiomBlocks")
        sense_blocks = self.soup.find_all('div', class_='vocabulary-top_multipleSense__wX134')      # 每条释义
        for _, sense in enumerate(sense_blocks):
            chunk_group = sense.find('div', class_="vocabulary-chunk_group__FrAQ9 vocabulary-chunk_inline__uWEOK vocabulary-top_eng__VWJ54")
            if chunk_group:
                temp = chunk_group.find_all('span', class_="vocabulary-chunk_root__sjfAa vocabulary-chunk_bold__Cb0D1")
                en = ""
                simp = ""
                for i in temp:
                    if i["data-tag"] == "eng":
                        en += i.get_text(strip=True) + " "
                    elif i["data-tag"] == "simp":
                        simp += i.get_text(strip=True)
                define["chunk_group"]["eng"] = en.replace("  ", " ")
                define["chunk_group"]["simp"] = simp.strip()
                # print(define)
                result["definitions"].append(copy.deepcopy(define))
                define = {
                "chunk_group":{
                    "eng":  "str",
                    "simp": "str",
                    },
                }
        for _ in result["definitions"]:
            # print(_)
        
            # if sense.name == "div" and sense.class_ == "vocabulary-top_cutTitle__Urc10":      # 当前释义的分组  
            #     chunk_group = sense.find_all('span', class_="vocabulary-chunk_root__sjfAa vocabulary-chunk_bold__Cb0D1")
            #     for chunk in chunk_group:
            #         if isinstance(chunk, Tag):
            #             if 'data-search-key' in chunk.attrs:
            #                 match chunk["data-tag"]:
            #                     case "eng":
            #                         define["chunk_group"]["eng"] = chunk.get_text(strip=True)
            #                     case "simp":
            #                         define["chunk_group"]["simp"] = chunk.get_text(strip=True)
            # elif sense.name == "div" and sense.class_ == "vocabulary-top_sense__Fja-g":
                
            pass

# 提取词性释义
def extract_definitions(soup):
    """提取单词的各个释义和例句"""
    definitions = []

    # 找到所有释义块
    sense_blocks = soup.find_all('div', class_='vocabulary-top_multipleSense__wX134')


    print(" =============== sense_blocks =============== ")
    for sense_block in sense_blocks:
        definition_data = {}
        symbol_keys = []  # 用于存储所有 symbol keys
        data_symbol_keys = []

        defines = []
        # 提取释义编号
        sense_number_elem = sense_block.find('div', id='define')
        define = {
            "sense_number": "",
            "gram_key": "",
            "symbol_key": "",
            "search_key": "",
            "definition_en": "",
            "definition_cn": "",
        }
        if sense_number_elem:
            # 获取第一个文本节点作为释义编号
            data_search_key = ""
            for child in sense_number_elem.children:
                if isinstance(child, Tag):
                    
                    # # 检查是否有 data-symbol-key 属性
                    # if child.has_attr('data-symbol-key'):
                    #     symbol_key = child['data-symbol-key']
                    #     symbol_keys.append(symbol_key)
                    #     print(f"找到 data-symbol-key: {symbol_key}")
                
                    # 你也可以获取其他属性
                    if 'data-search-key' in child.attrs:
                        data_search_key += child['data-search-key']
                        define["search_key"] = data_search_key
                    if "data-gram-key" in child.attrs:
                        define["gram_key"] = child['data-gram-key']
                        data_search_key += child['data-gram-key']
                        define["search_key"] = data_search_key
                    if "data-symbol-key" in child.attrs:
                        define["symbol_key"] = child['data-symbol-key']
            defines.append(define)
        define = {
            "sense_number": "",
            "gram_key": "",
            "symbol_key": "",
            "search_key": "",
            "definition_en": "",
            "definition_cn": "",
        }

        print(defines)
        
        # # 提取释义内容
        # definition_text = []
        # chinese_text = []
        
        # # 查找释义中的英文和中文部分
        # all_spans = sense_block.find_all('span', class_='vocabulary-chunk_root__sjfAa')
        # for span in all_spans:
        #     # 检查是否有data-chinese属性
        #     if 'data-chinese' in span.attrs:
        #         if span['data-chinese'] == 'true':
        #             chinese_text.append(span.get_text(strip=True))
        #         elif span['data-chinese'] == 'false':
        #             definition_text.append(span.get_text(strip=True))
        
        # # 合并释义文本
        # definition_data['definition_en'] = ' '.join(definition_text)
        # definition_data['definition_cn'] = ' '.join(chinese_text)
        
        # # 提取例句
        # examples = []
        # example_list = sense_block.find('ul', class_='vocabulary-top_exampleList__j+ZMa')
        
        # if example_list:
        #     example_items = example_list.find_all('li')
        #     for item in example_items:
        #         example_data = {}
                
        #         # 提取英文例句
        #         eng_example = item.find('div', class_='vocabulary-top_exampleEng__I2cLd')
        #         if eng_example:
        #             # 获取所有文本内容
        #             example_data['english'] = eng_example.get_text(' ', strip=True)
                
        #         # 提取中文例句
        #         chn_example = item.find('div', class_='vocabulary-top_exampleSimp__W5ybk')
        #         if chn_example:
        #             example_data['chinese'] = chn_example.get_text(' ', strip=True)
                
        #         if example_data:
        #             examples.append(example_data)
        
        # definition_data['examples'] = examples
        # definitions.append(definition_data)
    
    return definitions

# 提取搜索历史
def extract_search_history(soup):
    """提取搜索历史记录"""
    history = []
    history_section = soup.find('div', class_='desktop-header_history__obzHr')
    
    if history_section:
        history_items = history_section.find_all('span', class_='desktop-header_item__xgfeG')
        for item in history_items:
            history.append(item.get_text(strip=True))
    
    return history

# 提取用户信息
def extract_user_info(soup):
    """提取用户信息"""
    user_info = {}
    
    # 提取电话号码
    phone_elem = soup.find('span', class_='desktop-header_phone__ZYyuQ')
    if phone_elem:
        user_info['phone'] = phone_elem.get_text(strip=True)
    
    return user_info

# 主函数
def _main():
    # 提取所有信息
    word_info = extract_word_basic_info(soup)
    # print(word_info)    

    definitions = extract_definitions(soup)
    # print(definitions[0])

    search_history = extract_search_history(soup)
    user_info = extract_user_info(soup)
    
    # 组合所有数据
    result = {
        'word_info': word_info,
        'definitions': definitions,
        'search_history': search_history,
        'user_info': user_info
    }
    
    # # 打印结果
    # print("=" * 50)
    # print("单词基本信息:")
    # print(f"单词: {word_info.get('word', 'N/A')}")
    # print(f"词性: {word_info.get('part_of_speech', 'N/A')}")
    # print(f"发音: {word_info.get('pronunciation', {})}")
    # print(f"标签: {', '.join(word_info.get('symbols', []))}")
    
    # print("\n" + "=" * 50)
    # print("详细释义:")
    # for i, definition in enumerate(definitions, 1):
    #     print(f"\n释义 {definition.get('sense_number', i)}:")
    #     print(f"  英文释义: {definition.get('definition_en', 'N/A')}")
    #     print(f"  中文释义: {definition.get('definition_cn', 'N/A')}")
        
    #     if definition.get('examples'):
    #         print(f"  例句:")
    #         for j, example in enumerate(definition['examples'], 1):
    #             print(f"    {j}. 英文: {example.get('english', 'N/A')}")
    #             print(f"       中文: {example.get('chinese', 'N/A')}")
    
    # print("\n" + "=" * 50)
    # print(f"搜索历史: {', '.join(search_history)}")
    
    # print("\n" + "=" * 50)
    # print(f"用户信息: {user_info}")
    
    # # 将结果保存为JSON文件
    # with open('word_grand_info.json', 'w', encoding='utf-8') as f:
    #     json.dump(result, f, ensure_ascii=False, indent=2)
    
    # print("\n" + "=" * 50)
    # print("数据已保存到 word_grand_info.json 文件")

def main():
    processer = OxfordDictProcessor()

    word_header = processer.extract_word_header()
    processer.extract_definitions()

if __name__ == "__main__":
    main()