import os
import pandas as pd
from apps import LedgerTable,StockTable,DataBaseInit,StockCodeTable
import os
import pandas as pd
import plotly.express as px

def comp_list_w_list(list_,c_lists_,dict_id):
    temp = []
    for u in c_lists_:
        c_u = u[dict_id]
        flag = True
        for c in list_:
            c = c[dict_id]
            if c_u == c:
                flag = False
        if flag:
            temp.append(u)
    return temp

if __name__ == "__main__":
    host = 'db'
    user = 'root'
    pw = os.environ.get('MARIADB_ROOT_PASSWORD')
    ledge_db = os.environ.get('MDASH__database__NAME')
    public_db = 'public'
    print(pw)
    sql = DataBaseInit(host,user,pw)
    user_c = os.environ.get('MDASH__database__USER')
    user_p = os.environ.get('MDASH__database__PASSWD') 
    ledger = LedgerTable(host,user,pw,ledge_db)
    stock = StockTable(host,user,pw,public_db)
    stockcode = StockCodeTable(host,user,pw,public_db)
    dbs = sql.getListDataBase()

    c_dbs = [
        {'Database':ledge_db},
        {'Database':public_db}
    ]

    users = sql.getListUsers()

    c_users = [
        {'User':user_c,'pw':user_p }
    ]

    c_users = comp_list_w_list(users,c_users,'User')
    
    if len(c_users)>0:
        for c in c_users:
            sql.createUser(c['User'],c['pw'],'%')
    
    c_dbs = comp_list_w_list(dbs,c_dbs,'Database')
    if len(c_dbs)>0:
        print(c_dbs)
        for l in c_dbs:
            sql.createDB(l['Database'])

    ledger.connection()
    ledger.create_table()

    stock.connection()
    stock.create_table()

    stockcode.connection()
    stockcode.create_table()
    
    stock.grant(user_c,user_p,'all privileges')
    ledger.grant(user_c,user_p,'all privileges')
    stockcode.grant(user_c,user_p,'all privileges')

    # ledger = LedgerTable(host,user_c,user_p,ledge_db)
    # ledger.showGrant()
    # stock = StockTable(host,user_c,user_p,public_db)
    # stock.showGrant()

    # sql.create_table()
    # sql.create_table() 
    # sql = StockTable(config)
    # sql.create_table()