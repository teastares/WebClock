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
    def __init__(self, user):
        self.account = get_account(user)
        self.headers = get_headers()
        self.spider = Spider()
        self.courses = {}

    def login(self):
        self.spider.login(urls.login, self.account, self.headers)

    def is_logged(self):
        html = self.spider.session.get(urls.courses).text
        if len(html) >= 500:
            return True
        else:
            return False

    def get_courses(self, db):
        """
        To get the courses for one student, from the database
        If database can not find any course, get the courses from the website,
        and then save it in the database
        info[0] -> course_id, str
        info[1] -> name, str
        info[2] -> url, str
        """
        sql = "select course_id, course_name, course_url, course_enable,\
               notice_enable, homework_enable, file_enable from Course \
               where Course.user_id = '%s'" % (self.account['userid'])
        result = db.fetch_all(sql)
        if not result:
            self.spider.get_html(urls.courses)
            for info in parse.get_courses(self.spider.html):
                self.courses[info[0]] = Course(info[0], info[1], info[2])
                sql = "insert into Course(course_id, course_name, user_id, course_enable, \
                       notice_enable, homework_enable, file_enable, course_url) \
                       values ('%s', '%s', '%s', '%d', '%d', '%d', '%d', '%s')" % \
                       (info[0], info[1], self.account['userid'], 1, 1, 1, 1, info[2])
                db.update(sql)
        else:
            for info in result:
                self.courses[info[0]] = Course(info[0], info[1], info[2], info[3], info[4], info[5], info[6])

    def get_news(self):
        """
        To get to know how many new notice,
        file, and homework are there in the web.
        info[0] -> course_id, str
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
    def __init__(self, course_id, name, url, enable_course = 1, enable_notice = 1, enable_hw = 1, enable_file = 1):
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
        self.file = {}
        self.enable_course = enable_course
        self.enable_hw = enable_hw
        self.enable_notice = enable_notice
        self.enable_file =enable_file

    def get_newhomework(self, spider, user, db):
        """
        Get the information for homework, from the database
        and then ask for more information for homework from the website
        do some needed issue
        and then compare them to see if the database should be renew

        info[0] -> homework id, str
        info[1] -> url, str
        info[2] -> title, str
        info[3] -> state, str
        info[4] -> deadline, str
        """

        spider.get_html(urls.homework + self.course_id)
        for info in parse.get_newhomework(spider.html):
            sql = "select deadline, send_state, alarm_state from Homework \
                   where course_id = '%s' and homework_id = '%s' and user_id = '%s'" \
                   % (self.course_id, info[0], user[0])
            data = db.fetch_all(sql)
            if not data:
                deadline = datetime.strptime(info[4] + '-23-59-59', "%Y-%m-%d-%H-%M-%S")

                #for every homework, [url, title, deadline, send_state, alarm_state]
                if deadline > datetime.today() and info[3] == "尚未提交":
                    self.homework[info[0]] = [info[1], info[2],deadline, 0, 0]
                    sql = "insert into Homework(course_id, homework_id, url, \
                           homework_name, deadline, send_state, alarm_state, user_id) \
                           values ('%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s')" \
                           %(self.course_id, info[0], info[1], info[2], deadline, 0, 0, user[0])
                    db.update(sql)
            else:
                if data[0][0] < datetime.today() or info[3] == "已经提交":
                    sql = "delete from Homework where course_id = '%s' and homework_id = '%s' and \
                    user_id = '%s'" % (self.course_id, info[0], user[0])
                    db.update(sql)
                else:
                    self.homework[info[0]] = [info[1], info[2], data[0][0], data[0][1], data[0][2]]


    def send_newhomework(self, spider, user, db):
        for key, homework in self.homework.items():
            if homework[3] == 0:
                spider.get_html(urls.homework_detail + homework[0])
                info = parse.get_homeworkdetail(spider.html)
                if info == '':
                    info = 'NULL'
                title = '【' + 'New HomeWork ' + self.name +  '】' + homework[1]
                text = 'Instruction:\n' + info + '\n\n'
                text += 'Deadline:\n' + str(homework[2])
                mail.send_to_email(title, text, user[2])
                homework[3] = 1
                sql = "update Homework set send_state = '%d' \
                       where course_id = '%s' and homework_id = '%s' and user_id = '%s'" \
                       % (homework[3], self.course_id, key, user[0])
                db.update(sql)

    def alarm_homework(self, user, db):
        for key, homework in self.homework.items():
            residual_time = (homework[2] - datetime.today()).total_seconds()
            title = '【' + 'Homework Alarm ' + self.name +  '】' + homework[1]
            text = 'Deadline:\n' + str(homework[2]) + '\n\n'

            if residual_time <= 10800 and homework[4] <= 2:
                text += 'The residual time is less than 3 hours.\n\n'
                mail.send_to_email(title, text, user[2])
                homework[4] = 3
            elif residual_time <= 43200 and homework[4] <= 1:
                text += 'The residual time is less than 12 hours.\n\n'
                mail.send_to_email(title, text, user[2])
                homework[4] = 2
            elif residual_time <= 172800 and homework[4] == 0:
                text += 'The residual time is less than 48 hours.\n\n'
                mail.send_to_email(title, text, user[2])
                homework[4] = 1

            sql = "update Homework set alarm_state = '%d' \
                   where course_id = '%s' and homework_id = '%s' and user_id = '%s'" \
                   % (homework[4], self.course_id, key, user[0])
            db.update(sql)

    def get_newfile(self, spider, user, db):
        """
        Get the information for file,
        info[0] -> file id, str
        info[1] -> url, str, not used in this time but can be used in next time that help develop a function to send the file it self to the email
        info[2] -> title, str
        info[3] -> detail, str
        info[4] -> size, str
        info[5] -> send state, str, to indicate whether it is send or not, 0 indicates it hasn't been sent
        info[6] -> update date
        """
        spider.get_html(urls.files + self.course_id)
        for info in parse.get_newfile(spider.html, self.enable_file):
            sql = "select file_id, course_id, send_state from File \
                   where course_id = '%s' and file_id = '%s' and user_id = '%s'" \
                   % (self.course_id, info[0], user[0])
            data = db.fetch_all(sql)
            """
            Only record the files that less than 2 days.
            """
            update_date = datetime.strptime(info[6], "%Y-%m-%d")
            delta_time = (datetime.today() - update_date).total_seconds()
            if (not data) and (delta_time <= 172800):
                sql = "insert into File(file_id, course_id, send_state, user_id) \
                       values ('%s', '%s', '%d', '%s')" \
                       %(info[0], self.course_id, info[5], user[0])
                db.update(sql)
                if info[0] not in self.file:
                    self.file[info[0]] = [info[1], info[2], info[3], info[4], info[5]]
            elif data:
                if info[0] not in self.file:
                    self.file[info[0]] = [info[1], info[2], info[3], info[4], data[0][2]]


    def send_newfile(self, spider, user, db):
        """
        Send the information that new files have been put in the website
        If the information has been sent, then change the status to 1
        """
        for key, newfile in self.file.items():
            if newfile[4] == 0:
                title = '【' + 'New File ' + self.name + '】' + newfile[1]
                text = 'Detail: \n\n    ' + newfile[2] + '\n\n'
                text += 'File size: \n\n    ' + newfile[3] + '\n\n'
                mail.send_to_email(title, text, user[2])
                self.file[key][4] = 1
                sql = "update File set send_state = '%d' \
                       where course_id = '%s' and file_id = '%s' and user_id = '%s'" \
                       % (1, self.course_id, key, user[0])
                db.update(sql)

    def send_newnotice(self, spider, user):
        spider.get_html(urls.notice + self.course_id)
        for notice in parse.get_newnotice(spider.html, self.news[1], self.enable_notice):
            url = urls.notice_detail + notice[0]
            spider.get_html(url)
            detail = parse.get_noticedetail(spider.html)
            title = '【' + 'New Notice ' + self.name +  '】' + notice[1]
            text = 'author: \n' + notice[2] + '\n\n'
            text += 'detail: \n' + detail
            mail.send_to_email(title, text, user[2])


    def __str__(self):
        return self.name

def get_account(user):
    """
    """
    account = {}
    account['userid'] = user[0]
    account['userpass'] = user[1]
    account['useremail'] = user[2]
    return account

def get_headers():
    """
    get the headers information from the /resources/header.json file.
    """
    headers = json.load(open('resources/headers.json'))
    return headers
