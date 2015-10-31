#!/usr/bin/python3
import setting
import util
import re
import time

if __name__ == '__main__':

    student = util.Student()
    student.login()
    student.get_courses()
    while True:
        student.get_news()
        for course in student.courses.values():
            if setting.Enable_Hw == 1 and course.news[0] > 0:
                course.get_newhomework(student.spider)
                course.send_newhomework(student.spider)
                course.alarm_homework()

            if (setting.Enable_Notice == 1 and course.news[1] > 0) or setting.Enable_Notice == 2:
                course.send_newnotice(student.spider)

            if setting.Enable_File == 1 and course.news[2] > 0:
                course.send_newfile(student.spider)

        time.sleep(setting.Idle_Time)
