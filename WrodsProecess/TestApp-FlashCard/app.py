from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import random

app = Flask(__name__)

class FlashcardSystem:
    def __init__(self):
        self.word_repo = None
        self.card_details = None
        self.load_data()
    
    def load_data(self):
        """加载CSV数据"""
        try:
            self.word_repo = pd.read_csv('LexiconiaApp/data/WordRepository.csv')
            self.card_details = pd.read_csv('LexiconiaApp/data/CardDetails.csv')
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_card_data(self, num=None):
        

        """获取单词卡数据"""
        if self.word_repo is None or self.card_details is None:
            self.load_data()
        
        # 如果未指定序列号，随机选择一个
        if num is None:
            num = random.choice(self.word_repo['Num'].tolist())
        # 获取单词基本信息
        word_data = self.word_repo[self.word_repo['Num'] == int(num)].iloc[0]
        
        
        
        # 获取单词的多个释义（可能有多个词性）
        card_definitions = self.card_details[self.card_details['Root'] == num]
        
        definitions_list = []
        for _, definition in card_definitions.iterrows():
            definitions_list.append({
                'level': definition['Level'],
                'part_of_speech': definition['Part of Speech'],
                'addition': definition['addition'] if pd.notna(definition['addition']) and definition['addition'] != '-' else '',
                'explanation_e': definition['ExplainationE'] if pd.notna(definition['ExplainationE']) and definition['ExplainationE'] != '-' else '',
                'explanation_c': definition['ExplainationC'] if pd.notna(definition['ExplainationC']) and definition['ExplainationC'] != '-' else ''
            })
        
        return {
            'word': word_data['WordB'],
            'serial': num,
            'definitions': definitions_list
        }
    
    def get_all_cards(self):
        """获取所有卡片序列号用于导航"""
        if self.word_repo is None:
            self.load_data()
        return self.word_repo['Num'].tolist()

flashcard_system = FlashcardSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/card')
def get_card():
    print(" ========== 2 ========== ")
    num = int(request.args.get('serial'))
    card_data = flashcard_system.get_card_data(num)
    return jsonify(card_data)

@app.route('/api/cards/list')
def get_cards_list():
    print(" ========== 1 ========== ")
    cards_list = flashcard_system.get_all_cards()
    return jsonify(cards_list)

if __name__ == '__main__':
    app.run(debug=True)