import pymysql

class DataBase:
    def __init__(self, env_dict):
        host = env_dict['host']
        user = env_dict['user']
        pw = env_dict['password']
        db = env_dict['db']

        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=pw,
                                    db=db,
                                    charset='utf8')

    def __del__(self):
        if 'conn' in dir(self):
            self.conn.close()
            print("close connect")

    def get_id(self):
        format_ = self.config['table']
        return list(format_.keys())

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("SHOW TABLES")
        table_name = self.config['table_name']
        # fetch all the matching rows
        result = cur.fetchall()
        if table_name not in result:
            print("create table")
            format_ = self.config['table']
            table_dict = format_.keys()
            ids = ""
            for table_ in table_dict:
               ids += (str(table_)+" ")
               ids += (str(format_[table_])+",")
            # ids += "PRIMARY KEY ('idx'),"
            ids = ids[:-1]
            # print(ids)
            cur.execute("CREATE TABLE {} ({})".format(table_name, ids))

    def insert_table(self, table_):
        table_name = self.config['table_name']
        format_ = self.config['table']
        table_dict = list(format_.keys())

        cur = self.conn.cursor()
        temp = ""
        for i in range(len(table_dict)):
            f_ = format_[table_dict[i]]
            temp += "'" if 'char' in f_ else ""
            temp += "{}"
            temp += "'" if 'char' in f_ else ""
            temp += ','
        temp = temp[:-1]

        for row in table_:
            t = temp.format(*row)
            cur.execute("INSERT INTO {} VALUES({})".format(table_name, t))
        self.conn.commit()