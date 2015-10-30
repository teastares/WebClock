#!/usr/bin/python3
import util
import re
import time

if __name__ == '__main__':

    student = util.Student()
    student.login()
    student.get_courses()
    while True:
        student.get_news()
        time.sleep(5)
