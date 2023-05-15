import pymysql
import pandas as pd
import datetime

class DataBaseInit:
    def __init__(self,host,user,pw):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=pw,
                                    port=3306,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor) 
        self.cursor = self.conn.cursor()
    # Define a method to create MySQL users
    def createUser(self, userName, password,host,
                   querynum=0, 
                   updatenum=0, 
                   connection_num=0):
        try:
            sqlCreateUser = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s';"%(userName,host, password)
            self.cursor.execute(sqlCreateUser)
            self.cursor.execute('FLUSH PRIVILEGES;;')
        except Exception as Ex:
            print("Error creating MySQL User: %s"%(Ex))



    def getListDataBase(self,show=False):
        mySqlListUsers = "show databases;"
        self.cursor.execute(mySqlListUsers)
        dbList = self.cursor.fetchall()
        if show:
            print("List of users:")
            for db in dbList:
                print(db)
        return dbList 

    def createDB(self,dbName):
        try:
            sql_cmd = f'create database {dbName} default character set utf8mb4;'
            self.cursor.execute(sql_cmd)
        except Exception as Ex:
            print("Error creating MySQL User: %s"%(Ex))
    
    def dropDB(self,dbName):
        try:
            sql_cmd = f'drop database {dbName}'
            sql_cmd += ";"
            self.cursor.execute(sql_cmd)
        except Exception as Ex:
            print("Error creating MySQL User: %s"%(Ex))

    def getListUsers(self,show=False):
        mySqlListUsers = "select host, user from mysql.user;"
        self.cursor.execute(mySqlListUsers)
        userList = self.cursor.fetchall()
        if show:
            print("List of users:")
            for user in userList:
                print(user)
        return userList

class DataBase:
    def __init__(self, host,user,pw,db):
        self.host =host
        self.user =user
        self.pw   =pw 
        self.db   =db  
        self.table_query = {
            "date": 'DATE',
            "comment": 'varchar(40)',
            "amount": 'float',
            "category": 'varchar(20)',
            "input": 'varchar(30)',
            "output": 'varchar(30)'
        }
        self.conn = None
        self.cursor = None
        self.view_list = None
        self.connection()

    def connection(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.pw,
                                    db=self.db,
                                    port=3306,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.conn.cursor()
        except:
            self.conn = None
            self.cursor = None
            print("connection fail")

    def __del__(self):
        if 'conn' in dir(self) and self.conn is not None:
            self.conn.close()
            print("close connect")

    def showGrant(self,show=True):
        self.cursor.execute(f'select * from {self.db}.{self.table_name};;')
        grantsList = self.cursor.fetchall()
        if show:
            print("List of grants:")
            for grants in grantsList:
                print(grants)
        return grantsList

    def grant(self,user,pw,grant_list,with_grant=False,show=False):
        # all privileges == select, insert, delete, update, references
        if isinstance(grant_list,list):
            grant_w = ','.join(grant_list)
        else:
            grant_w = grant_list
        
        w_grant = ""
        if with_grant:
            w_grant += 'with grant option'

        try:
            sql_cmd = f'grant {grant_w} on {self.db}.{self.table_name} to {user}'
            sql_cmd = sql_cmd + (' ' + w_grant if with_grant else "") +";"
            self.cursor.execute(sql_cmd)
            self.cursor.execute('flush privileges;')
            if show:
                self.showGrant()

        except Exception as Ex:
            print("Error granting MySQL User: %s"%(Ex))

    def check_view(self):
        sql = "SHOW FULL TABLES IN hschoi WHERE TABLE_TYPE LIKE 'VIEW';"
        cur = self.conn.cursor()
        cur.execute(sql)
        return list(dict(cur.fetchall()).keys())

    def get_id(self):
        format_ = self.table_query
        return list(format_.keys())

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("SHOW TABLES")
        table_name = self.table_name
        # fetch all the matching rows
        result = cur.fetchall()
        if self.key is not None:
            key = ","+self.key
        else:
            key = ""

        if len(result)>0:
            result = result[0]
        else:
            result = None

        if (result is None) or table_name not in result.values():
            format_ = self.table_query
            table_dict = format_.keys()
            ids = ""
            for table_ in table_dict:
               ids += (str(table_)+" ")
               ids += (str(format_[table_])+",")
            # ids += "PRIMARY KEY ('idx'),"
            ids = ids[:-1]
            # print(ids)
            cur.execute("CREATE TABLE {} ({} {})".format(table_name, ids, key))

    def insert_table(self, table_):
        table_name = self.table_name
        format_ = self.table_query
        table_dict = list(format_.keys())
        if 'id' in table_dict:
            table_dict.remove('id')

        cur = self.conn.cursor()
        temp = ""
        valuel = "("
        for dic in table_dict:
            valuel += dic +", "

        valuel = valuel[:-2]
        valuel += ")"

        for i in range(len(table_dict)):
            f_ = format_[table_dict[i]]
            temp += "'" if 'char' in f_ else ""
            temp += "{}"
            temp += "'" if 'char' in f_ else ""
            temp += ','
        temp = temp[:-1]

        for row in table_:
            data_ = []
            if isinstance(row,dict):
                row = list(row.values())
            data_.extend(row)
            for i in range(len(data_)):
                if isinstance(data_[i],datetime.date):
                    data_[i] = data_[i].strftime("%Y-%m-%d")
                    data_[i] = str(data_[i]).replace('-','')

            if  True in (pd.isna(data_)):
                print("sure")
            else:
                t = temp.format(*data_)
                sql = "INSERT INTO {} {} VALUES({});".format(table_name,valuel, t)
                print(sql)
                cur.execute(sql)
        self.conn.commit()

    def send_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

    def create_view(self, view_name, query):
        if view_name not in self.view_list:
            sql = "CREATE VIEW {} AS {};".format(view_name, query)
            cur = self.conn.cursor()
            cur.execute(sql)
