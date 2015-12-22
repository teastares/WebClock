import pymysql
import setting

class database(object):
    def __init__(self):
        self._dbhost = setting.db_host
        self._dbpassword = setting.db_passwd
        self._dbuser = setting.db_user
        self._dbname = setting.db_database
        self._dbport = setting.db_port
        self._dbcharset = setting.db_charset
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

    def new_user(self, user_id, user_passwd, user_email):
        """
        Default set the user state to -1 (do not scan).
        """
        sql = "INSERT INTO User (user_id, user_passwd, user_email, user_state) \
               VALUES ('%s', '%s', '%s', '%d')" % (user_id, user_passwd, user_email, -1)
        self.update(sql)

    def validate_user(self, user_id, user_passwd):
        sql = "SELECT * FROM User WHERE user_id = '%s' AND user_passwd = '%s'" \
               % (user_id, user_passwd)
        data = self.fetch_all(sql)
        return data

    def get_user(self, user_id):
        sql = "SELECT user_id, user_email, user_state FROM User WHERE user_id = '%s'" \
               % user_id
        data = self.fetch_all(sql)
        return data[0]

    def get_courses(self, user_id):
        sql = "SELECT course_id, course_name, course_enable FROM Course WHERE user_id = '%s'" \
               % user_id
        data = self.fetch_all(sql)
        return data

    def get_course_from_id(self, user_id, course_id):
        sql = "SELECT * FROM Course WHERE user_id = '%s' AND course_id = '%s'" \
               % (user_id, course_id)
        data = self.fetch_all(sql)
        return data[0]

    def get_homework(self, user_id, course_id):
        sql = "SELECT * FROM Homework WHERE user_id = '%s' AND course_id = '%s'" \
               % (user_id, course_id)
        data = self.fetch_all(sql)
        return data


    def switch(self, user_id, state):
        sql = "UPDATE User SET user_state = %d \
               WHERE user_id = '%s'" % (state, user_id)
        self.update(sql)

    def course_enable(self, user_id, course_id, state):
        sql = "UPDATE Course SET course_enable = %d WHERE user_id = '%s' AND \
               course_id = '%s'" %(state, user_id, course_id)
        self.update(sql)

    def notice_enable(self, user_id, course_id, state):
        sql = "UPDATE Course SET notice_enable = %d WHERE user_id = '%s' AND \
               course_id = '%s'" %(state, user_id, course_id)
        self.update(sql)

    def homework_enable(self, user_id, course_id, state):
        sql = "UPDATE Course SET homework_enable = %d WHERE user_id = '%s' AND \
               course_id = '%s'" %(state, user_id, course_id)
        self.update(sql)

    def file_enable(self, user_id, course_id, state):
        sql = "UPDATE Course SET file_enable = %d WHERE user_id = '%s' AND \
               course_id = '%s'" %(state, user_id, course_id)
        self.update(sql)

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
