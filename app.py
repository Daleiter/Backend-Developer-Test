from flask import Flask, request, render_template, make_response,send_file,redirect, url_for
from service.db import login_user, register_user, create_post, get_post, del_post
import hashlib
import sys
from flask_restful import Api
import jwt
from datetime import datetime, timedelta
import random


app = Flask(__name__)
api = Api(app)
secret_key = 'test123'


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/logining', methods=['POST'])
def logining():
    data = request.form.to_dict()
    passw_hash = hashlib.md5(data['passw'].encode()).hexdigest()
    passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
    userdata = login_user(data['user'],passw_hash)
    if userdata:
        return userdata.token
    else:
        return "login fails"
    
@app.route('/registering', methods=['POST'])
def registering():
    data = request.form.to_dict()
    passw_hash = hashlib.md5(data['passw'].encode()).hexdigest()
    passw_hash = hashlib.md5(passw_hash.encode()).hexdigest()
    try:
        payload = {
            'username': data['user'],
            'exp': datetime() + timedelta(days=1)  # Задайте термін дії токену
                }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        if register_user(data['user'], passw_hash, token):
            return token
        else:
            return 'error mysql'
    except:
        return 'error'
   
@app.route('/addpost', methods=['POST'])
def addpost():
    data = request.form.to_dict()
    try:
        decoded_token = jwt.decode(data["token"], secret_key, algorithms=['HS256'])
    except:
        return "auth error"
    if sys.getsizeof(data["posttest"]) > 512:
        return "size error"
    else:
        id = random.randint(1, 100)
        if create_post(id, data["posttest"], decoded_token["username"]):
            return id
        else:
            return "error mysql"
    
@app.route('/getpost', methods=['POST'])
def getpost():
    data = request.form.to_dict()
    try:
        decoded_token = jwt.decode(data["token"], secret_key, algorithms=['HS256'])
    except:
        return "auth error"
    postlist = get_post(decoded_token["username"])
    if postlist:
        return postlist
    return "Null post"

@app.route('/delpost', methods=['POST'])
def delpost():
    data = request.form.to_dict()
    try:
        decoded_token = jwt.decode(data["token"], secret_key, algorithms=['HS256'])
    except:
        return "auth error"
    del_status = del_post(data["post_id"])
    return del_status

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')
