#!/usr/bin/python3
from resources import urls
import requests
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
        self.course_id = course_id
        self.name = name
        self.url = urls.base + url
        self.news = [0, 0, 0]

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
