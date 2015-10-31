#!/usr/bin/python3
from resources import urls
from datetime import datetime
import requests
import mail
import json
import re
import parse

class Spider(object):
    """
    This is a general spider to get the information from the web,
    with the login function.
    """
    def __init__(self):
        self.session = requests.session()
        self.html = ''

    def login(self, url, data, headers = None):
        if headers == None:
            self.session.post(url, data = data)
        else:
            self.session.post(url, data = data, headers = headers)

    def get_html(self, url):
        self.html = self.session.get(url).text
        return self.html

class Student(object):
    """
    Student is the class that describe the user of this software.
    It includes the information like account of the user,
    the courses of the user and so on.
    """
    def __init__(self):
        self.account = get_account()
        self.headers = get_headers()
        self.spider = Spider()
        self.courses = {}

    def login(self):
        self.spider.login(urls.login, self.account, self.headers)

    def get_courses(self):
        """
        To get the courses for one student,
        info[0] -> course_id, int
        info[1] -> name, str
        info[2] -> url, str
        """
        self.spider.get_html(urls.courses)
        for info in parse.get_courses(self.spider.html):
            self.courses[info[0]] = Course(info[0], info[1], info[2])

    def get_news(self):
        """
        To get to know how many new notice,
        file, and homework are there in the web.
        info[0] -> course_id, int
        info[1] -> new homework, int
        info[2] -> new notice, int
        info[3] -> new file, int
        """
        self.spider.get_html(urls.courses)
        for info in parse.get_news(self.spider.html):
            self.courses[info[0]].news = info[1:]

class Course(object):
    """
    Course stores the information about a specific course,
    including its url, course name, and the number of new notice\
    new homework\ new files.
    """
    def __init__(self, course_id, name, url):
        """
        news[0] -> new homework, int
        news[1] -> new notice, int
        news[2] -> new file, int
        """
        self.course_id = course_id
        self.name = name
        self.url = urls.base + url
        self.news = [0, 0, 0]
        #for every homework, [url, title,deadline, send_state, alarm_state]
        self.homework = {}

    def get_newhomework(self, spider):
        """
        Get the information for homework,
        info[0] -> homework id, int
        info[1] -> url, str
        info[2] -> title, str
        info[3] -> state, str
        info[4] -> deadline, str
        """
        spider.get_html(urls.homework + str(self.course_id))
        for info in parse.get_newhomework(spider.html):
            deadline = datetime.strptime(info[4] + '-23-59-59', "%Y-%m-%d-%H-%M-%S")
            if deadline < datetime.today() or info[3] == "已经提交":
                if info[0] in self.homework:
                    del self.homework[info[0]]

            elif info[0] not in self.homework:
                #for every homework, [url, title, deadline, send_state, alarm_state]
                self.homework[info[0]] = [info[1], info[2],deadline, 0, 0]

    def send_newhomework(self, spider):
        for homework in self.homework.values():
            if homework[3] == 0:
                spider.get_html(urls.homework_detail + homework[0])
                info = parse.get_homeworkdetail(spider.html)
                if info == '':
                    info = 'NULL'
                title = '【' + 'New HomeWork ' + self.name +  '】' + homework[1]
                text = 'Instruction:\n' + info + '\n\n'
                text += 'Deadline:\n' + str(homework[2])
                mail.send_to_email(title, text)
                homework[3] = 1

    def alarm_homework(self):
        for homework in self.homework.values():
            residual_time = (homework[2] - datetime.today()).total_seconds()
            title = '【' + 'Homework Alarm ' + self.name +  '】' + homework[1]
            text = 'Deadline:\n' + str(homework[2]) + '\n\n'
            if homework[4] == 0 and residual_time <= 172800:
                text += 'The residual time is less than 48 hours.\n\n'
                mail.send_to_email(title, text)
                homework[4] += 1
            elif homework[4] == 1 and residual_time <= 43200:
                text += 'The residual time is less than 12 hours.\n\n'
                mail.send_to_email(title, text)
                homework[4] += 1
            elif homework[4] == 2 and residual_time <= 10800:
                text += 'The residual time is less than 3 hours.\n\n'
                mail.send_to_email(title, text)
                homework[4] += 1

    def send_newnotice(self, spider):
        spider.get_html(urls.notice + str(self.course_id))
        for notice in parse.get_newnotice(spider.html, self.news[1]):
            url = urls.notice_detail + notice[0]
            spider.get_html(url)
            detail = parse.get_noticedetail(spider.html)
            title = '【' + 'New Notice ' + self.name +  '】' + notice[1]
            text = 'author: \n' + notice[2] + '\n\n'
            text += 'detail: \n' + detail
            mail.send_to_email(title, text)

    def send_newfile(self, spider):
        pass

    def __str__(self):
        return self.name

def get_account():
    """
    get the account information from the /resources/account.json file,
    if you don't alter the file, you'll be asked to enter it in terminal.
    """
    account = json.load(open('resources/account.json'))
    if account['userid'] == '*' or account['userpass'] == '*':
        account['userid'] = input("Student Number: ")
        account['userpass'] = input("Password: ")
    return account

def get_headers():
    """
    get the headers information from the /resources/header.json file.
    """
    headers = json.load(open('resources/headers.json'))
    return headers
