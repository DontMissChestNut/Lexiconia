import pandas as pd
import os

word_list_path = [
    "./WordList/A1.txt",
    "./WordList/A2.txt",
    "./WordList/B1.txt",
    "./WordList/B2.txt",
    "./WordList/C1.txt",
    "./WordList/C2.txt"
    ]

CEFR_csv_address_ = "./Assets/CEFRWordList_w.csv"
CEFR_csv_word_address_ = "./Assets/CEFRWordList_word.csv"
CEFR_csv_phrace_address_ = "./Assets/CEFRWordList_phrace.csv"
CEFR_csv_MyWords_address_ = "./Assets/MyWords_.csv"
CEFR_csv_MyPhraces_address_ = "./Assets/MyPhraces_.csv"
CEFR_csv_Root_address_ ="./Assets/Root.csv"

word_form_CEFR = {
    "Root": "string",
    "Serial" : "string",
    "Word": "string",
    "Guideword" : "string",
    "Level": "string",
    "Part of Speech": "string",
    "Topic": "string"
}

Level = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
    "-":  9
}

PartofSpeech = {
    "adjective":        1,
    "adverb":           2,
    "auxiliary verb":   3,
    "conjunction":      4, 
    "determiner":       5,
    "exclamation":      6,
    "modal verb":       7,
    "noun":             8,
    "number":           9,
    "preposition":      10,
    "pronoun":          11,
    "verb":             12,
    "phrase":           21,
    "phrasal verb":     22,
}

class Processer:
    def __init__(self):
        pass
        
    def openTXT(self, address):
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
        phrace_list_processed = []
        for _ in word_list:
            word = {
                "Root": "-",
                "Serial" : "-",
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
                if word["Part of Speech"] == "phrase" or word["Part of Speech"] == "phrasal verb":
                    phrace_list_processed.append(word)
                else:
                    word_list_processed.append(word)

        return word_list_processed, phrace_list_processed

    def writeCSV(self, address, data):
        # 检查文件是否存在
        # file_exists = os.path.isfile(address)
        
        # 创建DataFrame
        df = pd.DataFrame(columns=['Root', "Serial", 'Word', "Guideword", "Level","Part of Speech", "Topic"])
        
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
        df.to_csv(address, mode="w", index=False, encoding="utf-8", header=True)
        
        return

class CardGenerator:
    def __init__(self):
        pass

    def ReadCEFRWordListCSV(self, path, word_from):
        df = pd.read_csv(
            path,
            encoding="utf-8",
            header=0
        )
        
        words = []
        cards = []
        for i in range(len(df)):
            # print(df["Word"][i])
            word = df["Word"][i]
            
            card = {
                "Root": df["Root"][i],
                "Serial" : "-",
                "Word": df["Word"][i],
                "Guideword" : df["Guideword"][i],
                "Level": df["Level"][i],
                "Part of Speech": df["Part of Speech"][i],
                "Topic": df["Topic"][i]
            }
            
            words.append(word)
            cards.append(card)
            
        words_set = list(set(words))
        words_set.sort()
            
        return words_set, cards

def main():
    # processWordList()
    
    generateCard()
    
    return 

def SaveMyWord(words):
    save_path = "./Assets/MyWordList.csv"
    
    l = []
    d = {}
    for i, v in enumerate(words):
        
        word = {
            "Root": "-",
            "Serial": "00-0000-0-0",         # Level - SortedIndex - Part of Speech - SubIndex
            "Word": "-"
        }
        word["Root"] = "{:0>4d}".format(i + 1)
        word["Serial"] = "00-{:0>4d}-0-0".format(i + 1)
        word["Word"] = v
        
        l.append(word)
        d[v] = "{:0>4d}".format(i + 1)
        


    return l, d
    
    
def processWordList():
    processer = Processer()
    
    for path in word_list_path:
        word_list, phrace_list = processer.openTXT(path)
        processer.writeCSV(CEFR_csv_word_address_, word_list)
        processer.writeCSV(CEFR_csv_phrace_address_, phrace_list)
    
def generateCard():
    generator = CardGenerator()

    words, cards = generator.ReadCEFRWordListCSV(CEFR_csv_word_address_, word_form_CEFR)
    _, phraceCards = generator.ReadCEFRWordListCSV(CEFR_csv_phrace_address_, word_form_CEFR)
    
    l, d = SaveMyWord(words)
    
    cur_word = ""
    cursor = 0
    for c in cards:
        if c["Word"] != cur_word:
            cur_word = c["Word"] 
            cursor = 1
        else:
            cursor += 1
        level = Level[c["Level"]]
        serial = d[c["Word"]]
        p = PartofSpeech[c["Part of Speech"]]
        sub_index = cursor
        
        card_serial = "{:0>2d}-{}-{:0>2d}-{:0>1d}".format(level, serial, p, sub_index)
        
        c["Root"] = d[c["Word"]]
        c["Serial"] = card_serial
        
    for pc in phraceCards:
        if pc["Root"] == "-":
            pc["Root"] = "0000"
        level = Level[pc["Level"]]
        serial = pc["Root"]
        p = PartofSpeech[pc["Part of Speech"]]
        sub_index = "0"
        
        card_serial = "{:0>2d}-{}-{:0>2d}-{}".format(level, serial, p, sub_index)
        pc["Serial"] = card_serial
    
    # 创建DataFrame
    df = pd.DataFrame(columns=['Root', "Serial", 'Word', "Guideword", "Level","Part of Speech", "Topic"])
    
    df = pd.concat([df, pd.DataFrame(cards)], ignore_index=True)
    df.to_csv(CEFR_csv_MyWords_address_, mode="w", index=False, encoding="utf-8", header=True)
    
    df2 = pd.DataFrame(columns=['Root', "Serial", 'Word', "Guideword", "Level","Part of Speech", "Topic"])
    
    df2 = pd.concat([df2, pd.DataFrame(phraceCards)], ignore_index=True)
    df2.to_csv(CEFR_csv_MyPhraces_address_, mode="w", index=False, encoding="utf-8", header=True)


    df3 =  pd.DataFrame(columns=["Root", "Serial", 'Word'])
    df3 = pd.concat([df3, pd.DataFrame(l)], ignore_index=True)
    df3.to_csv(CEFR_csv_Root_address_, mode="w", index=False, encoding="utf-8", header=True)
    

if __name__ == "__main__":
    main()