import pymysql
import setting

class database(object):
    def __init__(self, host, user, passwd, db, port, charset):
        self._dbhost = host
        self._dbuser = user
        self._dbpassword = passwd
        self._dbname = db
        self._dbport = int(port)
        self._dbcharset = charset        
        self._conn = self.connectMySQL()
        if(self._conn):
            self._cursor = self._conn.cursor()


    def connectMySQL(self):
        conn = False
        try:
            conn = pymysql.connect(host = self._dbhost,
                    user = self._dbuser,
                    passwd = self._dbpassword,
                    db = self._dbname,
                    port = self._dbport,
                    charset = self._dbcharset,
                    )
        except Exception:
            print("Database Connecting Failed!")
            conn = False
        return conn


    #get result requry set
    def fetch_all(self, sql):
        res = ''
        if(self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception:
                res = False
                print("Database Query Failed!")
        return res

        
    def update(self, sql):
        flag = False
        if(self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception:
                flag = False
                print("Database Update Failed!")
        return flag

    #close the database
    def close(self):
        if(self._conn):
            try:
                if(type(self._cursor)=='object'):
                    self._cursor.close()
                if(type(self._conn)=='object'):
                    self._conn.close()
            except Exception:
                print("close database exception")   
   
        
    def get_user(self):
        sql = "select user_id, user_passwd, user_email from User"
        return self.fetch_all(sql)
    