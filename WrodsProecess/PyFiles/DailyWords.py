import pandas as pd

path = ".\Assets\WordList.csv"
path_root = ".\Assets\Root.csv"
path_to_review = ".\Assets\ToReview.csv"

CEFR_csv_Root_address_ ="./Assets/Root.csv"
CEFR_csv_MyWords_address_ = "./Assets/MyWords_.csv"

# The Ebbinghaus Forgetting Curve
TEFC  = ("5min", "30min", "12h", "1d", "2d", "4d", "7d", "15d")  # 8 nodes

def main():
    df = pd.read_csv(
        path,
        encoding="utf-8",
        header=0
    )
    
    words = []
    for i in range(len(df)):
        # print(df["Word"][i])
        word = df["Word"][i]
        
        words.append(word)
    
    df2 = pd.read_csv(
        path_root,
        encoding="utf-8",
        header=0
    )
    
    root = {}
    for i in range(len(df2)):
        root[df2["Word"][i]] = "{:0>4d}".format(int(df2["Root"][i]))
        
    addition_count = len(df2) + 342
    
    word_list = []
    root_additon = []
    word_addition = []
    for _ in words:
        w = dict()
        if _ in root.keys():
            w["Root"] = root[_]
        else:
            w["Root"] = addition_count
            ra = {
                "Root": addition_count,
                "Serial": "09-{:0>4d}-01-1".format(int(w["Root"])),         # Level - SortedIndex - Part of Speech - SubIndex
                "Word": _
            }
            wa = {
                "Root": addition_count,
                "Serial": "09-{:0>4d}-01-1".format(int(w["Root"])),         # Level - SortedIndex - Part of Speech - SubIndex
                "Word": _,
                "Guideword": "-", 
                "Level": "-",
                "Part of Speech": "-", 
                "Topic": "-"
            }
            addition_count += 1
            
            root_additon.append(ra)
            word_addition.append(wa)
            
        w["Serial"] = "00-{:0>4d}-0-0".format(int(w["Root"]))
        w["Word"] = _
        w["CurNode"] = -2,
        w["CurTime"] = "YYYY-MM-DD-hh-mm-ss"
        w["NextTime"] = "YYYY-MM-DD-hh-mm-ss"
        
        word_list.append(w)
        
    wdf = pd.DataFrame(columns=['Root', "Serial", 'Word', "CurNode", "CurTime","NextTime"])
    
    wdf = pd.concat([wdf, pd.DataFrame(word_list)], ignore_index=True)
    wdf.to_csv(path_to_review, mode="w", index=False, encoding="utf-8", header=True)
    
    radf = pd.DataFrame(columns=["Root", "Serial", 'Word'])
    
    radf = pd.concat([radf, pd.DataFrame(root_additon)], ignore_index=True)
    radf.to_csv(CEFR_csv_Root_address_, mode="a", index=False, encoding="utf-8", header=False)
    
    wadf = pd.DataFrame(columns=['Root', "Serial", 'Word', "Guideword", "Level","Part of Speech", "Topic"])
    
    wadf = pd.concat([wadf, pd.DataFrame(word_addition)], ignore_index=True)
    wadf.to_csv(CEFR_csv_MyWords_address_, mode="a", index=False, encoding="utf-8", header=False)
    
    
        
    return 

if __name__ == "__main__":
    main()