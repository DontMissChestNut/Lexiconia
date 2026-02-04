"""
WordRepositoryManager 管理单词库
- 包含单词序号、英式、美式
"""
word_repository_form = {
    "num": "string",
    "word_b": "string",
    "word_a": "string",
}

"""
CardDetailsManager 管理有道卡片详情
- 包含单词序号、等级、词性、添加信息、英文解释、中文解释
"""
word_card_form_youdao= {
    "root": "string",
    "serial" : "10-000000-00-0",        # youdao(1)+level - root - part of speech - num
    "level": "string",
    "part_of_speech": "string",
    "addition": "string",           # 名词复数、动词变形等
    "explaination_e": "string",
    "explaination_c": "string",
    # "Phonetic": "string"          # TODO： 音标
}

"""
MyReviewManager 管理单词的复习记录
- 包含单词序号、当前节点、当前时间、下一次复习时间
"""
word_to_review_form = {
    "root": "-",
    "Word": "-",
    "CurNode": -1,
    "CurTime": "YYYY-MM-DD-hh-mm-ss",
    "NextTime": "YYYY-MM-DD-hh-mm-ss"
}

"""
PathGraphManager 管理单词的路径图
- 只包含相关单词
"""
path_graph_form = {
    "node": "{:0>6d}".format(0),      # 当前单词节点
    "root": "{:0>6d}".format(0),      # 根词（step=-1），每个单词只有一个根词
    "step0": "string",                # 同根词（对称），存储为JSON数组
    "step1": "string",                # 同根不同义（非对称），存储为JSON数组
    "step2": "string",                # 近义词（对称），存储为JSON数组
    "step3": "string",                # 反义词（对称），存储为JSON数组
    "step4": "string",                # 形近词/音近词（对称），存储为JSON数组
}

detail_repo_form = {
    "root": "string",           # 单词序号 - 00000000
    "serial": "string",         # 详情序号 - 等级-词性-释义-词组
    "sentence": "string",       # 例句序号 - 00000000，例句才会有，否则为0
    "content" : "string",       # 内容
    "translation": "string",    # 翻译/解释
    "synonym": "string",        # 近义词（对称），详情序号（Serial），以;分割
    "antonym": "string",        # 反义词（对称），详情序号（Serial），以;分割
}