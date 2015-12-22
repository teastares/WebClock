#!/usr/bin/python3
import setting
import util
import re
import time
import random
import database

if __name__ == '__main__':

    while True:

        db = database.database(setting.db_host, setting.db_user, setting.db_passwd, setting.db_database, setting.db_port, setting.db_charset)
        db.connectMySQL()

        for user in db.get_user():
            """
            user:
            user[0] => user_id
            user[1] => user_passwd
            user[2] => user_email
            user[3] => user_state

            user_state:
            -1 => do not scan the user.
            0 => try to scan the user.
            1 => successful to login.
            2 => failed to login.
            """
            if user[3] == -1:
                continue

            student = util.Student(user)
            student.login()
            if student.is_logged():
                sql = "UPDATE User SET user_state = 1 \
                       WHERE user_id = '%s'" % user[0]
                db.update(sql)
                student.get_courses(db)
                student.get_news()

                for course in student.courses.values():

                    if course.enable_course == 1:
                        if course.enable_hw == 1 and  course.news[0]> 0:
                            course.get_newhomework(student.spider, user, db)
                            course.send_newhomework(student.spider, user, db)
                            course.alarm_homework(user, db)

                        if course.enable_notice == 1 and course.news[1] > 0:
                            course.send_newnotice(student.spider, user)

                        if course.enable_file == 1 and course.news[2] > 0:
                            course.get_newfile(student.spider, user, db)
                            course.send_newfile(student.spider, user, db)

            else:
                sql = "UPDATE User SET user_state = 2 \
                       WHERE user_id = '%s'" % user[0]
                db.update(sql)

        db.close()
