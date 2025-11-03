from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 单词列表（包含单词、音标、释义和例句）
word_list = [
    {
        "word": "apple",
        "phonetic": "/ˈæpl/",
        "meaning": "n. 苹果",
        "example": "I eat an apple every day."
    },
    {
        "word": "book",
        "phonetic": "/bʊk/",
        "meaning": "n. 书；v. 预订",
        "example": "I read an interesting book yesterday."
    },
    {
        "word": "computer",
        "phonetic": "/kəmˈpjuːtər/",
        "meaning": "n. 计算机，电脑",
        "example": "She works on her computer all day."
    },
    {
        "word": "diligent",
        "phonetic": "/ˈdɪlɪdʒənt/",
        "meaning": "adj. 勤奋的，刻苦的",
        "example": "He is a diligent student who always studies hard."
    },
    {
        "word": "enthusiasm",
        "phonetic": "/ɪnˈθjuːziæzəm/",
        "meaning": "n. 热情，热忱",
        "example": "She shows great enthusiasm for learning English."
    }
]

@app.route('/')
def index():
    # 渲染单词页面，传递第一个单词
    return render_template('word.html', word=word_list[0], total=len(word_list), current=1)

@app.route('/next_word/<int:current_index>')
def next_word(current_index):
    # 计算下一个单词的索引（循环）
    next_index = (current_index) % len(word_list)
    word_data = word_list[next_index]
    word_data['index'] = next_index + 1  # 从1开始的索引
    word_data['total'] = len(word_list)
    
    return jsonify(word_data)

if __name__ == '__main__':
    app.run(debug=True)