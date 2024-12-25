from flask import Blueprint, jsonify, request,session
from datetime import datetime
import database as db #共用Database連線

api = Blueprint('ajax_api',__name__,url_prefix="/ajax")#api路由

@api.route('/enter_park', methods=['POST'])
def enter_park():
    user_id = request.form.get('name')  # 取得從前端發送的 name 參數

    if user_id:
        # 將 user_id 存入 session
        session['user_id'] = user_id

        # 搜尋資料庫是否已經存在相同的 user_id
        existing_visitor = db.VisitorTable.find_one({'user_id': user_id})
        if existing_visitor:
            # 如果資料庫中已經存在該 user_id，則不重複新增
            # 更新入園狀態
            db.VisitorTable.update_one(
                    {'user_id': user_id},
                    {'$set': {'is_in_park': True}}  # 將 is_in_park 更新為 True
                )
            # 撈取使用者的餘額
            balance = existing_visitor.get('balance', 0)

            # 查詢用戶交易紀錄
            records = db.RecordsTable.find_one({'user_id': user_id})
            records = records.get('description', []) if records else []

            return jsonify({'status': 'success', 'message': '您已經成功入園！', 'balance': balance, 'records': records})
        
        # 如果不存在該 user_id，則新增該使用者到資料庫(第一次入園)
        visitor_data = {'user_id': user_id, 'is_in_park': True,"balance": 0}
        result = db.VisitorTable.insert_one(visitor_data)

        return jsonify({'status': 'success', 'balance': balance})
    else:
        return jsonify({'status': 'fail', 'message': '入園失敗！'})
    
@api.route('/leave_park', methods=['POST'])
def leave_park():
    user_id = session['user_id']
    # 退出園區時清除 session
    session.pop('user_id', None)  # 清除 session 中的 user_id
    # 更新入園狀態
    db.VisitorTable.update_one(
            {'user_id': user_id},
            {'$set': {'is_in_park': False}}  # 將 is_in_park 更新為 True
        )
    return jsonify({'status': 'success','user_id': user_id})

@api.route('/recharge', methods=['POST'])
def submit():
    amount = request.form.get('amount', type=int)  # 獲取儲值金額

    if amount and amount > 0:
        # 從 session 中獲取用戶的 ID (假設用戶已經登入，並且 user_id 存儲在 session 中)
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'status': 'fail', 'message': '請先登入'})

        # 查詢使用者資料
        result = db.VisitorTable.find_one({'user_id': user_id})

        if not result:
            return jsonify({'status': 'fail', 'message': '用戶不存在'})

        # 更新用戶餘額
        new_balance = result.get('balance', 0) + amount

        db.VisitorTable.update_one(
            {'user_id': user_id},
            {'$set': {'balance': new_balance}}
        )
        # 取得當前日期和時間
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        HistoryItem = f'{current_date}  成功儲值 NT$ {amount}，目前餘額為 NT$ {new_balance}'

        

        existing_visitor = db.RecordsTable.find_one({'user_id': user_id})
        if existing_visitor:
            # 如果資料庫中已經存在該 user_id，則不重複新增
            # 撈取使用者的餘額
            description = existing_visitor.get('description', 0)
            description.append(HistoryItem)

            db.RecordsTable.update_one(
                {'user_id': user_id},
                {'$set': {'description': description}} 
            )

        else:
            record = {
                'user_id': user_id,
                'description': [HistoryItem]
            }
            db.RecordsTable.insert_one(record)

        # 回傳新餘額
        return jsonify({'status': 'success', 'new_balance': new_balance})
    else:
        return jsonify({'status': 'fail', 'message': '儲值金額無效'})
