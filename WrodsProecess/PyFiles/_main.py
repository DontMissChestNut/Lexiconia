import pandas as pd
from WordListProcesser import Processer
# import crawler

txtAddress = "../Assets/Words.txt"
csvAddress_r = "../Assets/WordList.csv"
csvAddress_w = "../Assets/WordList_w.csv"
CEFR_csv_address_ = "./Assets/CEFRWordList_r.csv"

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

def main():
    processer = Processer()
    
    for path in word_list_path:
        word_list, phrace_list = processer.openTXT(path)
    
        processer.writeCSV(CEFR_csv_address_, word_list)
    
    
def openTXT(address):
    with open(address) as f:
        data = f.read()
        
        words = data.split(",")
        
        l = list()
        
        for i in words:
            i = i.replace(" ", "")
            if i:
                l.append(i)
            
        my_data_form["Word"] = list(tuple(l))
        
    return
    

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