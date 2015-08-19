#!/usr/bin/python3
import requests
import re

class Course(object):
    """
    Course store the information about a specific course,
    including its url, course name, and the number of  new notice\ 
    new homework\ new files.
    """
    def __init__(self,  course_name):
        self.course_name = course_name

    def get_id(self, id):
        self.id = id

    def get_news(self, news):
        #To store how many new information there is
        self.new_homework = int(news[0])
        self.new_notice = int(news[1])
        self.new_file = int(news[2])

    def __str__(self):
        return self.course_name

class Spider(object):
    """
    This is a general spider to get the information from the web,
    with the login function.
    """
    def __init__(self):
        self.session = requests.session()

    def login(self, url, data, headers = None):
        if headers == None:
            self.session.post(url, data = data)
        else:
            self.session.post(url, data = data, headers = headers)

    def gethtml(self, url):
        self.html = self.session.get(url).text
        return self.html
