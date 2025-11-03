from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# 模拟用户存储（实际项目中应使用数据库）
users = []

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    # 获取表单数据
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')
    
    # 基本验证
    if not username or not email or not password or not confirm_password:
        return jsonify({'success': False, 'message': '所有字段都是必填的'})
    
    if len(username) < 3:
        return jsonify({'success': False, 'message': '用户名至少需要3个字符'})
    
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码至少需要6个字符'})
    
    if password != confirm_password:
        return jsonify({'success': False, 'message': '两次输入的密码不一致'})
    
    # 检查用户名或邮箱是否已存在
    for user in users:
        if user['username'] == username:
            return jsonify({'success': False, 'message': '用户名已存在'})
        if user['email'] == email:
            return jsonify({'success': False, 'message': '邮箱已被注册'})
    
    # 保存用户（实际项目中应加密密码）
    users.append({
        'username': username,
        'email': email,
        'password': password  # 注意：实际项目中应对密码进行哈希处理
    })
    
    return jsonify({'success': True, 'message': '注册成功！'})

if __name__ == '__main__':
    app.run(debug=True)