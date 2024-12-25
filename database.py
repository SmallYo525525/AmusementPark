import pymongo
from flask import g
from config import config #環境設定檔

# 定義表連線全域變數
VisitorTable = None
RecordsTable = None

# 在應用上下文結束時自動,關閉資料庫連線
def DatabaseConnect():
    global VisitorTable,RecordsTable
    if 'db' not in g:
         # 如果 g 物件中還沒有資料庫連線，則建立連線並儲存於 g
        g.db = pymongo.MongoClient(config.DATABASE_URL)[config.DATABASE_NAME]
    # 更改資料表對應實例    
    VisitorTable=g.db['VisitorInformation']
    RecordsTable=g.db['VisitorTransactionRecords']

    return g.db


