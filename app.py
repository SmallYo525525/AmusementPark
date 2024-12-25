from flask import Flask, render_template,session
from api import api
import database as db
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.register_blueprint(api)

# 初始化資料庫連線
with app.app_context():
    db.DatabaseConnect()

@app.route('/', methods=['GET','POST'])
def home():
    user_id = session.get('user_id')
    if user_id:
        # 查詢用戶餘額
        result = db.VisitorTable.find_one({'user_id': user_id})
        balance = result.get('balance', 0)
        # 查詢用戶交易紀錄
        records = db.RecordsTable.find_one({'user_id': user_id})
        records = records.get('description', []) if records else []
    else:
        records = []
        balance = 0
    return render_template('index.html',user_id=user_id,balance=balance, records=records)

@app.route('/recharge')
def recharge():
    user_id = session.get('user_id')
    if user_id:
        result = db.VisitorTable.find_one({'user_id': user_id})
        balance = result.get('balance', 0)
    else:
        balance = 0
    return render_template('recharge.html',user_id=user_id,balance=balance)

@app.route('/consume')
def consume():
    user_id = session.get('user_id')
    return render_template('consume.html',user_id=user_id)

@app.route('/history')
def history():
    user_id = session.get('user_id')
    return render_template('history.html',user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)