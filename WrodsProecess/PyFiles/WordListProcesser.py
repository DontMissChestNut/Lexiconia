import pandas as pd
import os

word_list_path = ["./WordList/A1.txt",
                  "./WordList/A2.txt",
                  "./WordList/B1.txt",
                  "./WordList/B2.txt",
                  "./WordList/C1.txt",
                  "./WordList/C2.txt"]

word_form_CEFR = {
    "Root": "string",
    "Word": "string",
    "Guideword" : "string",
    "Level": "string",
    "Part of Speech": "string",
    "Topic": "string"
}

CEFR_csv_address_ = "./Assets/CEFRWordList_w.csv"

def main():
    for path in word_list_path:
        word_list = openTXT(path)
        writeCSV(CEFR_csv_address_, word_list)
    

def openTXT(address):
    word_list = []
    with open(address) as f:
        word = []
        for line in f:
            if line != "\n":
                word.append(line.split("\n")[0])
            else:
                word_list.append(word)
                word = []   
        word_list.append(word)
        
    word_list_processed = []
    for _ in word_list:
        word = {
            "Root": "-",
            "Word": "-",
            "Guideword" : "-",
            "Level": "-",
            "Part of Speech": "-",
            "Topic": "-"
        }
        cursor = 0
        for i, detail in enumerate(_):
            if i == 0:
                cursor = 0
                word["Word"] = detail

            elif detail in ["A1", "A2", "B1", "B2", "C1", "C2"]:
                cursor = i
                word["Level"] = detail
                
            elif cursor == 0:
                word["Guideword"] = detail
                
            else:
                if (i - cursor + 2) == 3:
                    word["Part of Speech"] = detail
                elif (i - cursor + 2) == 4:
                    word["Topic"] = detail
                    
        if(word):
            word_list_processed.append(word)

    return word_list_processed

def writeCSV(address, data):
    # 检查文件是否存在
    file_exists = os.path.isfile(address)
    
    print(file_exists)
    
    # 创建DataFrame
    df = pd.DataFrame(columns=['Root', 'Word', "Guideword", "Level","Part of Speech", "Topic"])
    
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_csv(address, mode="a", index=False, encoding="utf-8", header=not file_exists)
      
    return

    

if __name__ == "__main__":
    main()