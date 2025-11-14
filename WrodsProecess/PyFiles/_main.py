from operator import ne
import pandas as pd
from WordListProcesser import Processer
# import crawler

txtAddress = "./Assets/Words.txt"
csvAddress_r = "../Assets/WordList.csv"
csvAddress_w = "../Assets/WordList_w.csv"
CEFR_csv_address = "./Assets/CEFRWordList_r.csv"
to_review_csv_address = "./Assets/ToReview.csv"
word_repository_csv_address = "./Assets/WordRepository.csv"
card_details_csv_address = "./Assets/CardDetails.csv"

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
    "Part of Speech": "string",
    "Topic": "string"
}

word_repository_form = {
    "Num": "string",
    "Serial" : "string",
    "WordB": "string",
    "WordA": "string",
}

word_tree_form = {
    "Num": "string",
    "Root" : "string",
    "Curr": "string",
    "Leaf": "string",
    "Step": "int",
}

word_card_form= {
    "Root": "string",
    "Serial" : "string",
    "Level": "string",
    "Part of Speech": "string",
    "addition": "string",
    "ExplainationE": "string",
    "ExplainationC": "string"
}

def main():
    df = pd.read_csv(
        card_details_csv_address,
        encoding="utf-8",
        header=0
        )

    for i in range(len(df)):
        df["Root"][i] = str("{:0>6d}").format(int(df["Root"][i]))

        serial = df["Serial"][i].split("-")
        df["Serial"][i] = "{:0>2d}-{:0>6d}-{:0>2d}-{:0>1d}".format(int(serial[0]), int(serial[1]), int(serial[2]), int(serial[3]))

    new_df = pd.DataFrame(columns=df.columns)
    new_df = pd.concat([new_df, pd.DataFrame(df)], ignore_index=True)
    df.to_csv("./Assets/CardDetails2.csv", index=False, encoding="utf-8")

    

    
    
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