from operator import ne
import pandas as pd
from WordListProcesser import Processer
# import crawler

txtAddress = "./Assets/Words.txt"
csvAddress_r = "../Assets/WordList.csv"
csvAddress_w = "../Assets/WordList_w.csv"
CEFR_csv_address = "./Assets/CEFRWordList_r.csv"
to_review_csv_address = "./Assets/my_review.csv"
word_repository_csv_address = "./Assets/WordRepository.csv"
card_details_csv_address = "./Assets/CardDetails.csv"
card_details_youdao_csv_address = "./Assets/CardDetails_youdao.csv"

my_data_form = {
    "Root": "string",
    "Word": "string"
}

word_list_path = [
    "./WordList/A1.txt",
    "./WordList/A2.txt",
    "./WordList/B1.txt",
    "./WordList/B2.txt",
    "./WordList/C1.txt",
    "./WordList/C2.txt"
    ]



word_form_CEFR = {
    "Root": "string",
    "Serial" : "string",
    "Word": "string",
    "Guideword" : "string",
    "Level": "string",
    "part_of_speech": "string",
    "Topic": "string"
}

word_repository_form = {
    "Num": "string",
    "Serial" : "string",
    "WordB": "string",
    "WordA": "string"
}

word_tree_form = {
    "Num": "string",
    "Root" : "string",
    "Curr": "string",
    "Leaf": "string",
    "Step": "int"
}

word_card_form= {
    "Root": "string",
    "Serial" : "string",
    "Level": "string",
    "part_of_speech": "string",
    "addition": "string",
    "ExplainationE": "string",
    "ExplainationC": "string"
}

word_to_review_form = {
    "Root": "-",
    "Word": "-",
    "CurNode": -1,
    "CurTime": "YYYY-MM-DD-hh-mm-ss",
    "NextTime": "YYYY-MM-DD-hh-mm-ss"
}

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

def main():
    df_words = pd.read_csv(
        word_repository_csv_address,
        encoding="utf-8",
        header=0
        )
    
    print(df_words)


    # new_df = pd.DataFrame(df_review.columns)
    # new_df = pd.concat([new_df, pd.DataFrame(df_review)], ignore_index=True)
    # df_review.to_csv("./Assets/my_review2.csv", index=False, encoding="utf-8")

    

    
    
def openTXT(address):
    with open(address) as f:
        data = f.read()
        
        words = data.split(",")
        
        l = list()
        
        for i in words:
            i = i.split(" ")
            new_ = ""
            for _ in i:
                if _ != "":
                    new_ = new_ + " " + _
            if new_:
                l.append(new_)
            
        my_data_form["Word"] = list(tuple(l))
        
    return list(tuple(l))
    

def readCSV(address):
    df = pd.read_csv(
        address,
        encoding="utf-8",
        header=0
        )
    
    words = []
    for i in range(len(df)):
        # word = {
        #     "Root": df["Root"][i],
        #     "Word": df["Word"][i]
        # }
        
        word = df["Word"][i]
        words.append(word)
        
    return words
    
def writeCSV(address, data):
    # 创建空的DataFrame
    df = pd.DataFrame(columns=['Root', 'Word'])
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_csv(address, index=False, encoding="utf-8")
    
    return 
    

if __name__ == "__main__":
    main()