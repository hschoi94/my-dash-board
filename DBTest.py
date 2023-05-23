import os
import pandas as pd
from apps import LedgerTable,StockTable,DataBaseInit
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
            temp.append(c_u)
    return temp

if __name__ == "__main__":
    host = 'db'
    user = 'mdash'
    pw = 'mdash'#os.environ.get('DB_PASS')
    db = os.environ.get('DB_NAME')
    sql = DataBaseInit(host,user,pw,port=3306)
    # user_c = os.environ.get('DB_USER')
    # user_p = os.environ.get('DB_PASS') 
    # ledger = LedgerTable(host,user,pw,db)
    # dbs = sql.getListDataBase()

    # c_dbs = [
    #     {'Database':db}
    # ]

    # users = sql.getListUsers()

    # c_users = [
    #     {'User':user_c,'pw':user_p }
    # ]

    # c_users = comp_list_w_list(users,c_users,'User')
    # if len(c_users)>0:
    #     for c in c_users:
    #         sql.createUser(c['User'],c['pw'])
    
    # c_dbs = comp_list_w_list(dbs,c_dbs,'Database')
    # if len(c_dbs)>0:
    #     print(c_dbs)
    #     for l in c_dbs:
    #         sql.createDB(l)

    # ledger.connection()
    # ledger.create_table()
    # sql.grant(user_c,'all privileges')
    # ledger = LedgerTable(host,user_c,user_p,db)

    # sql.create_table()
    # sql.create_table() 
    # sql = StockTable(config)
    # sql.create_table()