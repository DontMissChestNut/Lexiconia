from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import random
from datetime import datetime, timedelta, time

# from models import CardDetailsManager, WordRepositoryManager, MyReviewManager, Crawler
from services import LexiconiaService

"""
Lexiconia App

work stream
===== Lexiconia =====


===== Add Words =====


===== Prepare Review Words =====


===== Review Words =====

"""


app = Flask(__name__)

updateTime = time(5, 0, 0)  # 05:00:00

lexiconia_service  = LexiconiaService()

""" =============== Guide Page =============== """

@app.route('/')
def guide():
    return render_template('_guidepage.html')

""" =============== Lexiconia =============== 
背单词页面 - daily review
"""

@app.route('/lexiconia')
def lexiconia():
    return render_template('lexiconia.html')

@app.route('/api/lexiconia')
def get_lexiconia():

    # due_reviews = lexiconia_service .get_daily_reviews()

    # 打印调试信息
    # print(f"Content-Type: {request.content_type}")
    # print(f"Headers: {dict(request.headers)}")
    # if('num' not in request.args):
    #     cards_list = lexiconia_system.get_all_cards()
    #     num = random.choice(cards_list)
    # else:
    #     num = int(request.args.get('num'))
    # card_data = lexiconia_system.get_card_data(num)
    # return jsonify(card_data)
    return render_template('lexiconia.html')

@app.route('/api/lexiconia/list')
def get_lexiconia_list():
    # cards_list = lexiconia_system.get_all_cards()
    # return jsonify(cards_list)
    return render_template('lexiconia.html')

""" =============== daily review =============== 
背单词页面 - daily review
"""

@app.route('/dailyreview')
def daily_review():
    return render_template('dailyreview.html')

@app.route('/api/dailyreview')
def get_daily_review():

    due_reviews = lexiconia_service .get_daily_reviews()

    print(due_reviews)

    if len(due_reviews) == 0:
        result_message = "暂无待复习单词"
        response_data = {
            'success': False,
            'message': result_message,
            'reviews': []
        }
    else:
        result_message = f"待复习复习： {len(due_reviews)} 个单词"
        response_data = {
            'success': True,
            'message': result_message,
            'reviews': due_reviews
        }

    return jsonify(response_data)

@app.route('/api/dailyreview/list')
def get_daily_review_list():
    due_reviews = lexiconia_service .get_daily_reviews()

    print(f"due_reviews: {due_reviews}")

    # for d in due_reviews:
    #     print(d["root"])
    
    if len(due_reviews) == 0:
        result_message = "暂无待复习单词"
        response_data = {
            'success': False,
            'message': result_message,
            'reviews': []
        }
    else:
        result_message = f"待复习复习： {len(due_reviews)} 个单词"
        response_data = {
            'success': True,
            'message': result_message,
            'reviews': due_reviews
        }
        
    return jsonify(response_data)

@app.route('/api/dailyreview/finish', methods=['POST', "GET"])
def finish_daily_review():
    if request.method == 'POST':
        data = request.get_json()
        root = data.get('root')

        if not root:
            return jsonify({'success': False, 'message': '请提供单词根词'}), 400
        
        # 处理完成单词的逻辑
        result = lexiconia_service .update_view_status_nodes(root)
        
        if result:
            return jsonify({'success': True, 'message': '单词已完成'})
        else:
            return jsonify({'success': False, 'message': '单词不存在于复习列表'})
    else:
        return jsonify({'success': False, 'message': '请使用 POST 方法'})

""" =============== Add Words =============== """

@app.route('/addwords')
def add_words():
    # print('add words')
    return render_template('addwords.html')

@app.route('/api/addwords', methods=['POST'])
def add_words_api():
    """处理添加单词的API"""
    try:
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
        
        if not words_string:
            return jsonify({'success': False, 'message': '请输入单词'})
        
        # 处理添加单词的逻辑

        result = lexiconia_service .add_words(words_string)

        print(f"result: {result}")
        
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

@app.route('/api/cards/list', methods=['POST', 'GET'])
def get_cards_list():
    """获取所有卡片序列号"""
    # cards_list = lexiconia_service .get_all_cards()
    cards_list = []
    return jsonify({'success': True, 'cards_list': cards_list})



""" =============== Prepare Review =============== """
@app.route('/addmyreview')
def add_my_review():
    return render_template('addmyreview.html')

@app.route('/api/addmyreview', methods=['POST'])
def add_my_words_api():
    """处理添加复习单词的API"""
    try:

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
        
        if not words_list:
            return jsonify({'success': False, 'message': '请输入单词'})
        
        # 处理添加单词的逻辑
        result = lexiconia_service .add_my_review(words_list)
        
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

@app.route('/preparereview')
def preparereview():
    return render_template('preparereview.html')

@app.route('/api/prepare_review_words')
def get_prepare_review_words():
    """获取需要准备的复习单词"""
    count = request.args.get('count', default=120, type=int)
    
    try:
        # 筛选状态为-1（未开始复习）的单词c
        # sample_words = lexiconia_service .prepare_my_review(count, "complex")
        sample_words = lexiconia_service .prepare_my_review(count, "youdao")

        words_list = []
        for word in sample_words:
            detail = ""
            for d in word["Details"]:
                detail = d["part_of_speech"] + " " + d["explaination_c"] + "\n"


            words_list.append({
                "root": word["root"],
                "word": word["Word"],
                "details": word["Details"]
                # "details": detail
            })
            
        
        return jsonify({
            'words': words_list,
            'total': len(words_list)
        })
        
    except Exception as e:
        return jsonify({'error': '获取单词失败'}), 500

@app.route('/api/update_review_list', methods=['POST'])
def update_review_list():
    # print(" =============== update_review_list =============== ")
    """更新复习列表，将选中的单词标记为今日复习"""
    # data = request.json
    if request.is_json:
            data = request.get_json()
    selected_root = data.get('selectedWords', [])
    
    # print([i["root"] for i in selected_root])           # 获取需要开始背的单词root序列
    
    try:
        count = lexiconia_service .start_review_0([i["root"] for i in selected_root])

        if(count == len(selected_root)):
            return jsonify({
                'status': 'success',
                'updated_count': count
            })
        elif(count != len(selected_root)):
            return jsonify({
                'status': 'Warning',
                'message': f'只有 {count} 个单词被更新'
            })
        
    except Exception as e:
        return jsonify({'error': '更新复习列表失败'}), 500

""" =============== Path Builder =============== """

@app.route('/pathbuilder')
def get_word_info():
    return render_template('pathbuilder.html')

""" api: 获取路径图 """
@app.route('/api/pathbuilder')
def api_get_graph_info():
    print(" =============== api_get_graph_info =============== ")

    graph, word_list = lexiconia_service.get_graph_info()
    return jsonify({'success': True, 'graph': graph, 'word_list': word_list})

""" api: 获取路径图 """
@app.route('/api/pathbuilder/<word>', methods=["POST", "GET"])
def api_get_word_info(word):
    print(" =============== word =============== ", word)

    num = lexiconia_service.get_num([word])
    print(" =============== num =============== ", num)
    # graph, word_list = lexiconia_service.get_graph_info()
    return jsonify({'success': True, 'num': num})


# @app.route('/api/pathbuilder/word/<root>')
# def get_word_info(root):
#     """获取单词详细信息"""
#     try:
#         word_info = lexiconia_service.get_word_info(root)
#         if word_info:
#             return jsonify({'success': True, 'data': word_info})
#         else:
#             return jsonify({'success': False, 'message': '单词未找到'})
#     except Exception as e:
#         return jsonify({'success': False, 'message': f'获取单词信息失败: {str(e)}'}), 500

# @app.route('/api/pathbuilder/search')
# def search_words():
#     """搜索单词"""
#     keyword = request.args.get('keyword', '')
#     try:
#         words = lexiconia_service.search_words(keyword)
#         return jsonify({'success': True, 'words': words})
#     except Exception as e:
#         return jsonify({'success': False, 'message': f'搜索失败: {str(e)}'}), 500

# @app.route('/api/pathbuilder/connection', methods=['POST'])
# def add_connection():
#     """添加单词连接"""
#     try:
#         data = request.get_json()
#         root = data.get('root')
#         point = data.get('point')
#         step = data.get('step')
        
#         if not all([root, point, step is not None]):
#             return jsonify({'success': False, 'message': '缺少必要参数'}), 400
        
#         success, message = lexiconia_service.add_word_connection(root, point, step)
#         return jsonify({'success': success, 'message': message})
        
#     except Exception as e:
#         return jsonify({'success': False, 'message': f'添加连接失败: {str(e)}'}), 500

# @app.route('/api/pathbuilder/connection', methods=['DELETE'])
# def delete_connection():
#     """删除单词连接"""
#     try:
#         data = request.get_json()
#         root = data.get('root')
#         point = data.get('point')
        
#         if not all([root, point]):
#             return jsonify({'success': False, 'message': '缺少必要参数'}), 400
        
#         success, message = lexiconia_service.delete_word_connection(root, point)
#         return jsonify({'success': success, 'message': message})
        
#     except Exception as e:
#         return jsonify({'success': False, 'message': f'删除连接失败: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)