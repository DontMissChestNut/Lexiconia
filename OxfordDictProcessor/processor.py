from bs4 import BeautifulSoup
import json
import re

# 读取HTML文件
with open('test.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 创建BeautifulSoup对象
soup = BeautifulSoup(html_content, 'html.parser')

# 提取单词基本信息
def extract_word_basic_info(soup):
    """提取单词基本信息：单词、音标、发音等"""
    result = {}
    
    # 提取单词本身
    word_elem = soup.find('span', class_='vocabulary-top_main__ibK-6')
    if word_elem:
        result['word'] = word_elem.get_text(strip=True)
    
    # 提取音标和发音
    pronunciation = {}
    pronunciation_chunks = soup.find_all('div', class_='vocabulary-top_chunk__4312R')
    if not pronunciation_chunks:
        pronunciation_chunks = soup.find_all('span', class_='vocabulary-top_chunk__4312R')
    
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
    
    # 提取词性标签
    pos_elem = soup.find('span', class_='vocabulary-top_pos__zpXHq')
    if pos_elem:
        result['part_of_speech'] = pos_elem.get_text(strip=True)
    
    # 提取单词等级标签（CET4, CET6等）
    symbols = []
    symbol_elems = soup.find_all('span', class_='vocabulary-top_symbol__xpmIs')
    for symbol_elem in symbol_elems:
        img_elem = symbol_elem.find('img')
        if img_elem and 'alt' in img_elem.attrs:
            symbols.append(img_elem['alt'])
    
    result['symbols'] = symbols
    
    return result

# 提取词性释义
def extract_definitions(soup):
    """提取单词的各个释义和例句"""
    definitions = []
    
    # 找到所有释义块
    sense_blocks = soup.find_all('div', class_='vocabulary-top_sense__Fja-g')[:1]
    

    print(" =============== sense_blocks =============== ")
    for sense_block in sense_blocks:
        definition_data = {}
        
        # 提取释义编号
        sense_number_elem = sense_block.find('div', id='define')
        if sense_number_elem:
            # 获取第一个文本节点作为释义编号
            sense_number = ''
            for child in sense_number_elem.children:
                print(child)
                if isinstance(child, str) and child.strip():
                    sense_number = child.strip()
                    break
            definition_data['sense_number'] = sense_number
        
        # 提取释义内容
        definition_text = []
        chinese_text = []
        
        # 查找释义中的英文和中文部分
        all_spans = sense_block.find_all('span', class_='vocabulary-chunk_root__sjfAa')
        for span in all_spans:
            # 检查是否有data-chinese属性
            if 'data-chinese' in span.attrs:
                if span['data-chinese'] == 'true':
                    chinese_text.append(span.get_text(strip=True))
                elif span['data-chinese'] == 'false':
                    definition_text.append(span.get_text(strip=True))
        
        # 合并释义文本
        definition_data['definition_en'] = ' '.join(definition_text)
        definition_data['definition_cn'] = ' '.join(chinese_text)
        
        # 提取例句
        examples = []
        example_list = sense_block.find('ul', class_='vocabulary-top_exampleList__j+ZMa')
        
        if example_list:
            example_items = example_list.find_all('li')
            for item in example_items:
                example_data = {}
                
                # 提取英文例句
                eng_example = item.find('div', class_='vocabulary-top_exampleEng__I2cLd')
                if eng_example:
                    # 获取所有文本内容
                    example_data['english'] = eng_example.get_text(' ', strip=True)
                
                # 提取中文例句
                chn_example = item.find('div', class_='vocabulary-top_exampleSimp__W5ybk')
                if chn_example:
                    example_data['chinese'] = chn_example.get_text(' ', strip=True)
                
                if example_data:
                    examples.append(example_data)
        
        definition_data['examples'] = examples
        definitions.append(definition_data)
    
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
def main():
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

if __name__ == "__main__":
    main()