from .database import DataBase

def account_sum(income, move_in, move_out, spend):
    keys = []
    keys.extend(list(income.keys()))
    keys.extend(list(move_in.keys()))
    keys.extend(list(move_out.keys()))
    keys.extend(list(spend.keys()))
    keys = list(set(keys))

    dict_ = dict()
    for key_ in keys:
        dict_[key_] = 0

    for in_c in income.keys():
        dict_[in_c] += income[in_c]
    for m_in in move_in.keys():
        dict_[m_in] += move_in[m_in]
    for m_out in move_out.keys():
        dict_[m_out] -= move_out[m_out]
    for s_out in spend.keys():
        dict_[s_out] -= spend[s_out]

    for k in keys:
        if abs(dict_[k]) < 0.00001:
            del dict_[k]
    return dict_


class LedgerTable(DataBase):
    def __init__(self, host,user,pw,db,table_name="ledger"):
        super(LedgerTable, self).__init__(host,user,pw,db)
        self.table_name = table_name
        self.table_query = {
            "date": 'DATE',
            "comment": 'varchar(40)',
            "amount": 'float',
            "category": 'varchar(20)',
            "input": 'varchar(30)',
            "output": 'varchar(30)',
            # "id":'NOT NULL AUTO_INCREMENT PRIMARY KEY'
        }


    def get_first_date(self):
        table_name = self.table_name
        cur = self.conn.cursor()
        sql = "SELECT * FROM {} ORDER BY date".format(table_name)
        cur.execute(sql)
        result = cur.fetchall()
        return result[0][0]

    def select_by_date(self, year=None, month=None):
        table_name = self.table_name
        cur = self.conn.cursor()
        import datetime
        today = datetime.date.today()
        state = 0
        if year is None:
            year = int(today.year)
            state += 1
        if month is None:
            month = int(today.month)
            state += 1

        search1 = int(year)*10000+month*100
        if state == 2:
            sql = "SELECT * FROM {} where date>{}".format(table_name, search1)
        else:
            search2 = int(year)*10000+(month+1)*100
            sql = "SELECT * FROM {} where {}<date AND date<{}".format(
                table_name, search1, search2)

        cur.execute(sql)
        result = cur.fetchall()
        return result

    def account_summary_view(self):
        def create_view(view_name, search_col, condition, group_by=None):
            if view_name not in self.view_list:
                gby_txt = 'GROUP BY {}'.format(
                    group_by) if group_by is not None else ""
                sql = "CREATE VIEW {} AS \
                SELECT input, SUM(amount) \
                FROM account \
                WHERE {}\
                {};".format(view_name, search_col, condition, gby_txt)
                cur = self.conn.cursor()
                cur.execute(sql)
        create_view("income", "input", "category = '수입'", "input")
        create_view("move_o", "output", "category = '이동'", "output")
        create_view("move_i", "input", "category = '이동'", "input")
        create_view("spend", "output",
                    "category != '이동' AND category != 수입", "output")

    def account_summary_from_quary(self):
        def get_account_q(inout, condition):
            sql = "SELECT {}, SUM(amount) \
            FROM account \
            WHERE {} \
            GROUP BY {};".format(inout, condition, inout)
            cur = self.conn.cursor()
            cur.execute(sql)
            return dict(cur.fetchall())

        income = get_account_q("input", "category = '수입'")
        move_out = get_account_q("output", "category = '이동'")
        move_in = get_account_q("input", "category = '이동'")
        spend = get_account_q(
            "output", "category != '이동' AND category != '수입'")
        res = account_sum(income, move_in, move_out, spend)
        return res

    def account_summary(self):
        def get_from_view(view_name):
            sql = "SELECT * FROM {};".format(view_name)
            cur = self.conn.cursor()
            cur.execute(sql)
            return dict(cur.fetchall())
        income = get_from_view("income")
        move_out = get_from_view("move_o")
        move_in = get_from_view("move_i")
        spend = get_from_view("spend")
        res = account_sum(income, move_in, move_out, spend)
        return res

    def create_view_monthly_summary(self):
        query = "SELECT category,SUM(amount) FROM account \
        WHERE\
            (DATE BETWEEN CONCAT(YEAR(NOW()), '-', MONTH(NOW()),'-',1) \
            AND LAST_DAY(CONCAT(YEAR(NOW()), '-', MONTH(NOW()),'-',1)))\
            AND (category!='이동' AND category!='수입')\
                GROUP BY category;"
        self.create_view('this_month', query)

        query = "SELECT category,SUM(amount) FROM account \
        WHERE\
            (DATE BETWEEN CONCAT(YEAR(NOW()), '-', MONTH(NOW())-1,'-',1) \
            AND LAST_DAY(CONCAT(YEAR(NOW()), '-', MONTH(NOW())-1,'-',1)))\
            AND (category!='이동' AND category!='수입')\
                GROUP BY category;"
        self.create_view('last_month', query)

    def get_last_update_date(self):
        query = "SELECT DATE FROM account ORDER BY DATE DESC LIMIT 1;"
        time = self.send_query(query)[0][0]
        return time

    def get_monthly_summary(self, yyyy=None, mm=None, minus=0):
        from datetime import datetime
        now = datetime.now()
        yyyy = yyyy if yyyy is not None else now.year
        mm = mm if mm is not None else now.month
        def prev_month(year,month,iter_num):
            date = f'{year}-{month}-1'
            yyyy = year
            mm = month
            if iter_num >0:
                for i in range(iter_num):
                    date_time = datetime.strptime(date, '%Y-%m-%d')
                    minus_ = datetime.timedelta(days=minus)
                    date_time = date_time-minus_
                    yyyy = date_time.year
                    mm = date_time.month
                    date = f'{yyyy}-{mm}-1'
            return yyyy,mm
        yyyy,mm = prev_month(yyyy,mm,minus)
        query = f"SELECT category,SUM(amount) FROM account \
        WHERE\
            (DATE BETWEEN CONCAT({yyyy}, '-', {str(mm).zfill(2)},'-',1) \
            AND LAST_DAY(CONCAT({yyyy}, '-', {str(mm).zfill(2)},'-',1)))\
            AND (category!='이동' AND category!='수입')\
                GROUP BY category;"
        return self.send_query(query)

