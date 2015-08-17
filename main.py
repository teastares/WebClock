#!/usr/bin/python3
from resources import urls
import util
import json
import requests
import re
import time
import mail
def get_account():
    """
    get the account information from the /resources/account.json file,
    if you don't alter the file, you'll be asked to enter it in terminal.
    """
    account = json.load(open('resources/account.json'))
    if account['userid'] == '*' or account['userpass'] == '*':
        print("Please enter your student's number:")
        account['userid'] = input()
        print("Please enter your password:")
        account['userpass'] = input()
    return account

def get_headers():
    """
    get the headers information from the /resources/header.json file.
    """
    headers = json.load(open('resources/headers.json'))
    return headers

class CourseSpider(util.Spider):
    """
    This is a spider to get the information of the NetCourses
    """
    def scan_courses(self, courses_list):
        self.login(urls.login, get_account(), get_headers())
        self.gethtml(urls.courses)
        courses_html = re.findall('<tr class="info_.*?</tr>', self.html.text, re.S)
        for course_html in courses_html:
            course = util.Course(re.search('target="_blank">(.*?)</a>', course_html, re.S).group(1).replace(' ', '').replace('\n', ''))
            url = re.search('<a href="(.*?)"', course_html, re.S).group(1)
            course.get_id(url[-6:])
            news = re.findall('red_text">(.*?)</', course_html, re.S)
            course.get_news(news)
            # To add this course into the courses_list
            courses_list.append(course)

    def scan_notice(self, course):
        notice_url = urls.notice + course.id
        self.gethtml(notice_url)
        #self.gethtml('http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp?course_id=112189')
        notices_html = re.findall('<tr class="tr.*?</tr>', self.html.text, re.S)
        #The variable "count" counts how many unread notices have been processed 
        count = 0
        for notice_html in notices_html:
            if count >= course.new_notice:
               break
            flag = re.findall("<td width='20%' align='center' height=25>(.*?)</td>", notice_html, re.S)[1]
            if flag == '未读':
                count += 1
                notice_url = 'http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/' + re.search("<a  href='(.*?)'>", notice_html, re.S).group(1)
                self.gethtml(notice_url)
                title = re.search('colspan="3">(.*?)</td>', self.html.text, re.S).group(1)
                text = re.search('overflow:hidden;">(.*?)&nbsp', self.html.text, re.S).group(1)
                self.send_to_email(title, text)

    def send_to_email(self, title, text):
        #This is the function to send the message to the email.
		mail_info = json.load(open('resources/mail_account.json'))
		mail_host = mail_info["host"]
		mail_user = mail_info["user"]
		mail_psw = mail_info["userpass"]
		to_user = mail_info["to_user"]
		if host == '*' or mail_user == '*' or mail_psw == "*":
			print("Please enter your mail's host"")
			mail_host = input()
			print("Please enter your mail's username:")
			mail_user = input()
			print("Please enter your mail's password:")
			mail_psw = input()
		if to_user == "*" ：
			print("plsase enter the mail you want to send")
			to_user = input()
		sender = mail.mail_sender(mail_host,mail_user,mail_psw)
		sender.sendmsg(title,text,to_user)
        pass

if __name__ == '__main__':

    spider = CourseSpider()
    while True:
        courses_list = []
        spider.scan_courses(courses_list)
        #To find the detail of each course
        for course in courses_list:
            if course.new_notice != 0:
                spider.scan_notice(course)

        time.sleep(60) 
