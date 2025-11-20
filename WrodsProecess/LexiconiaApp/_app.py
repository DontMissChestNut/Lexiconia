from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import random
from models import CardDetailsManager
from services import FlashcardService



app = Flask(__name__)

flashcard_service = FlashcardService()

@app.route('/')
def guide():
    return render_template('_guidepage.html')

@app.route('/lexiconia')
def lexiconia():
    return render_template('lexiconia.html')

@app.route('/addwords')
def add_words():
    # print('add words')
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
            # print(f"Raw data: {raw_data}")
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
        
        # print(f"Response: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        # print(f"Error adding words: {e}")
        import traceback
        # traceback.print_exc()
        return jsonify({'success': False, 'message': f'添加单词失败: {str(e)}'}), 500

@app.route('/addmyreview')
def add_my_review():
    print('add review')
    return render_template('addmyreview.html')

@app.route('/api/addmyreview', methods=['POST'])
def add_my_words_api():
    """处理添加复习单词的API"""
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
            # print(f"Raw data: {raw_data}")
            try:
                import json
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return jsonify({'success': False, 'message': '请使用 JSON 格式发送数据'}), 400
        
        words_list = data.get('words', '').split(',')
        print(f"Words list: {words_list}")
        
        if not words_list:
            return jsonify({'success': False, 'message': '请输入单词'})
        
        # 处理添加单词的逻辑
        result = flashcard_service.add_my_review(words_list)
        
        result_message = f"成功添加 {result['added_count']} 个单词"
        if result['false_count'] > 0:
            result_message += f"，跳过 {result['false_count']} 个不存在的单词"
        if result['skipped_count'] > 0:
            result_message += f"，跳过 {result['skipped_count']} 个已存在的单词"

        
        response_data = {
            'success': True,
            'message': result_message,
            'false': result['false'],
            'added': result['added'],
            'skipped': result['skipped']
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        # print(f"Error adding words: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'添加单词失败: {str(e)}'}), 500
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

import pandas as pd
import os
from datetime import datetime

@app.route('/preparereview')
def preparereview():
    return render_template('preparereview.html')

@app.route('/api/prepare_review_words')
def get_prepare_review_words():
    """获取需要准备的复习单词"""
    count = request.args.get('count', default=120, type=int)
    
    try:
        # 筛选状态为-1（未开始复习）的单词
        sample_words = flashcard_service.prepare_my_review(count)
        
        words_list = []
        for word in sample_words:
            words_list.append({
                "root": word["Root"],
                "word": word["Word"],
                "details": word["Details"]
            })
            
        
        return jsonify({
            'words': words_list,
            'total': len(words_list)
        })
        
    except Exception as e:
        print(f"获取准备复习单词失败: {e}")
        return jsonify({'error': '获取单词失败'}), 500

@app.route('/api/update_review_list', methods=['POST'])
def update_review_list():
    print(" =============== update_review_list =============== ")
    """更新复习列表，将选中的单词标记为今日复习"""
    # data = request.json
    if request.is_json:
            data = request.get_json()
    selected_root = data.get('selectedWords', [])
    
    print([i["root"] for i in selected_root])
    
    try:
        # 读取my_review.csv
        my_review_df = pd.read_csv('data/my_review.csv')
        
        # 更新选中的单词状态为1（今日复习），并设置复习日期
        today = datetime.now().strftime('%Y-%m-%d')
        for serial in selected_root:
            mask = my_review_df['serial'] == serial
            my_review_df.loc[mask, 'status'] = 1
            my_review_df.loc[mask, 'review_date'] = today
        
        # 保存更新后的CSV
        my_review_df.to_csv('data/my_review.csv', index=False)
        
        return jsonify({
            'status': 'success',
            'updated_count': len(selected_root)
        })
        
    except Exception as e:
        print(f"更新复习列表失败: {e}")
        return jsonify({'error': '更新复习列表失败'}), 500


if __name__ == '__main__':
    app.run(debug=True)