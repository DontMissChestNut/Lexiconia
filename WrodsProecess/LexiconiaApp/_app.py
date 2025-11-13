from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import random
from models import CardDetailsManager
from services import FlashcardService



app = Flask(__name__)



# flashcard_system = FlashcardSystem()

@app.route('/')
def guide():
    return render_template('_guidepage.html')

@app.route('/lexiconia')
def lexiconia():
    return render_template('lexiconia.html')

@app.route('/addwords')
def add_words():
    print('add words')
    return render_template('addwords.html')


@app.route('/api/addwords', methods=['POST'])
def add_words_api():
    """处理添加单词的API"""
    try:
        # 打印调试信息
        print(f"Received request: {request.method}")
        print(f"Content-Type: {request.content_type}")
        print(f"Headers: {dict(request.headers)}")
        
        if request.is_json:
            data = request.get_json()
        else:
            # 尝试从原始数据解析
            raw_data = request.get_data(as_text=True)
            print(f"Raw data: {raw_data}")
            try:
                import json
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return jsonify({'success': False, 'message': '请使用 JSON 格式发送数据'}), 400
        
        words_string = data.get('words', '')
        print(f"Words string: {words_string}")
        
        if not words_string:
            return jsonify({'success': False, 'message': '请输入单词'})
        
        # 处理添加单词的逻辑
        flashcard_service = FlashcardService()
        result = flashcard_service.add_words(words_string)
        
        result_message = f"成功添加 {result['added_count']} 个单词"
        if result['skipped_count'] > 0:
            result_message += f"，跳过 {result['skipped_count']} 个已存在的单词"
        
        response_data = {
            'success': True,
            'message': result_message,
            'added': result['added'],
            'skipped': result['skipped']
        }
        
        print(f"Response: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error adding words: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'添加单词失败: {str(e)}'}), 500

@app.route('/addmyreview')
def add_my_review():
    print('add review')
    return render_template('addmyreview.html')

@app.route('/api/addmyreview', methods=['POST'])
def add_my_words_api():

    return jsonify({'success': True, 'message': '添加单词成功'})

@app.route('/api/addcard')
def add_card():
    return render_template('addcard.html')

@app.route('/api/card')
def get_card():
    # if('num' not in request.args):
    #     cards_list = flashcard_system.get_all_cards()
    #     num = random.choice(cards_list)
    # else:
    #     num = int(request.args.get('num'))
    # card_data = flashcard_system.get_card_data(num)
    # return jsonify(card_data)
    return render_template('lexiconia.html')

@app.route('/api/cards/list')
def get_cards_list():
    # cards_list = flashcard_system.get_all_cards()
    # return jsonify(cards_list)
    return render_template('lexiconia.html')

if __name__ == '__main__':
    app.run(debug=True)