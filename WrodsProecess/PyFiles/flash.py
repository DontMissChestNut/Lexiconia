<<<<<<< HEAD
from flask import Flask
from flask import request, session, make_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
  return 'this is response of test function.'

@app.route('/user', methods = ['POST', 'GET'])
def get_users():
  if request.method == 'GET':
    return ... # 返回用户列表
  else:
    return ... # 创建新用户 

@app.route('/user/<int:uname>') # @app.route('/user/<uname>')
def get_userInfo(uname):
    return '%s\'s Informations' % uname

from flask import request, session, make_response

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            session['username'] = request.form['username']
            response = make_response('Admin login successfully!')
            response.set_cookie('login_time', time.strftime('%Y-%m-%d %H:%M:%S'))
            return 'Admin login successfully!'
        else:
            return 'No such user!'
    elif request.method == 'GET':
        if request.args.get("username") == 'admin':
            session['username'] = request.form['username']
            return 'Admin login successfully!'
        else:
            return 'No such user!'
        
app.secret_key = '123456'



if __name__ == '__main__':
=======
from flask import Flask
from flask import request, session, make_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
  return 'this is response of test function.'

@app.route('/user', methods = ['POST', 'GET'])
def get_users():
  if request.method == 'GET':
    return ... # 返回用户列表
  else:
    return ... # 创建新用户 

@app.route('/user/<int:uname>') # @app.route('/user/<uname>')
def get_userInfo(uname):
    return '%s\'s Informations' % uname

from flask import request, session, make_response

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            session['username'] = request.form['username']
            response = make_response('Admin login successfully!')
            response.set_cookie('login_time', time.strftime('%Y-%m-%d %H:%M:%S'))
            return 'Admin login successfully!'
        else:
            return 'No such user!'
    elif request.method == 'GET':
        if request.args.get("username") == 'admin':
            session['username'] = request.form['username']
            return 'Admin login successfully!'
        else:
            return 'No such user!'
        
app.secret_key = '123456'



if __name__ == '__main__':
>>>>>>> 79b72ed5e116e9bddc44cd9ec2d1bbf92c9cbb11
    app.run(debug=True)