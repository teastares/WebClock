#!/usr/bin/python3
import setting
import util
import re
import time
import random
import db

if __name__ == '__main__':
    
    db = db.database(setting.db_host, setting.db_user, setting.db_passwd, setting.db_database, setting.db_port, setting.db_charset)
    db.connectMySQL()
    while True:
        for user in db.get_user():
            student = util.Student(user)
            student.login()  
            student.get_courses(db)
            student.get_news()
            
            for course in student.courses.values():
                #print(course.name)
                #print(course.news)
                
                if course.enable_course == 1:  
                    #student.courses[course.course_id].news[0]
                    if course.enable_hw == 1 and  course.news[0]> 0:
                        #print(course.name)
                        course.get_newhomework(student.spider, db)
                        course.send_newhomework(student.spider, db)
                        course.alarm_homework(db)
                    
                    if (course.enable_notice == 1 and course.news[1] > 0) or course.enable_notice == 2:
                        course.send_newnotice(student.spider)

                    if course.enable_file == 1 and course.news[2] > 0:
                        #print(course.name)
                        #print("hello, I'm going to get the new file for the course!\n")
                        course.get_newfile(student.spider, db)
                        #print("hello, I'm going to send the new file for the course!\n")
                        course.send_newfile(student.spider, db)
                        #print("hello, I have completed for the course now!\n")

        time.sleep(setting.Idle_Time)
    
    db.close()
