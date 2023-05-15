import os
import numpy as np
from ledger.database import AccountDB
import pandas as pd

if __name__ == "__main__":
    account_dir_path = os.path.dirname(__file__)
    account_list_path = ["money.xlsx"]
    col_num = 0
    config = {
        "host":      "192.168.50.2",
        "user":      "hschoi",
        "password":  "z9wt6b!@",
        "db":        "hschoi",
    }
    sql = AccountDB(config)
    for account_path in account_list_path:
        file_path = os.path.join(account_dir_path, account_path)
        df = pd.read_excel(file_path)
        element = sql.get_id()
        index_ = []
        for e in element:
            for key in df.keys():
                if key in e:
                    index_.append(key)
                    break
        df = df[index_]
        table_ = np.array(df)
        col_num += len(table_)
        try:
            sql.insert_table(table_)
            print(sql.account_summary())
        except:
            print(file_path)
    print(col_num)
