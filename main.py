#!/usr/bin/python3
import util
import re
import time
import mail

if __name__ == '__main__':

    student = util.Student()
    student.login()
    student.get_courses()
    while True:
        student.get_news()
        for course in student.courses.values():
            if course.news[0] > 0:
                course.get_newhomework(student.spider)

        time.sleep(5)
