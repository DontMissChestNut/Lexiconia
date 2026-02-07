""" =============== FORMS =============== """

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
PathGraphManager 管理单词的路径图
- 只包含相关单词
"""
path_graph_form = {
    "node": "{:0>8d}".format(0),      # 当前单词节点
    "root": "{:0>8d}".format(0),      # 根词（step=-1），每个单词只有一个根词
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

""" =============== REMAPPING =============== """

LEVEL_REMAP_N2S = {
    "0": "--",
    "1": "A1",
    "2": "A2",
    "3": "B1",
    "4": "B2",
    "5": "C1",
    "6": "C2",
}

LEVEL_REMAP_S2N = {
    "--": "0",
    "A1": "1",
    "A2": "2",
    "B1": "3",
    "B2": "4",
    "C1": "5",
    "C2": "6",
}

PART_OF_SPEECH_REMAP_N2S = {
    "00": "--",
    "10": "n.",
    "11": "cn.",
    "12": "un.",
    "13": "pn.",
    "20": "v.",
    "21": "vt.",
    "22": "vi.",
    "30": "adj.",
    "40": "adv.",
    "50": "prep.",
    "60": "conj.",
    "70": "exclam.",
    "80": "art.",
    "90": "quant.",
}

PART_OF_SPEECH_REMAP_S2N = {
    "--": "00",
    "n.": "10",
    "cn.": "11",
    "un.": "12",
    "pn.": "13",
    "v.": "20",
    "vt.": "21",
    "vi.": "22",
    "adj.": "30",
    "adv.": "40",
    "prep.": "50",
    "conj.": "60",
    "exclam.": "70",
    "art.": "80",
    "quant.": "90",
}