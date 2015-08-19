#!/usr/bin/python3
from resources import urls
from bs4 import BeautifulSoup
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
        account['userid'] = input("Student Number: ")
        account['userpass'] = input("Password: ")
    return account

def get_headers():
    """
    get the headers information from the /resources/header.json file.
    """
    headers = json.load(open('resources/headers.json'))
    return headers

def send_to_email(title, text):
    """
    This is the function to send the message to the email.
    title refer to the title of the message,
    text is the main text of the message
    """
    mail_info = json.load(open('resources/mail_account.json'))
    mail_host = mail_info["host"]
    mail_user = mail_info["user"]
    mail_psw = mail_info["userpass"]
    to_user = mail_info["to_user"]
    if host == '*' or mail_user == '*' or mail_psw == "*":
        mail_host = input("Sending mail's host: ")
        mail_user = input("Sending mail's username: ")
        mail_psw = input("Sending mail's password: ")
    if to_user == "*" :
        to_user = input("Receiving mail: ")
    sender = mail.mail_sender(mail_host,mail_user,mail_psw)
    sender.sendmsg(title,text,to_user)

def scan_courses(html, courses_list):
    """
    This is the function to scan the courses of the courselist
    """
    courses_html = re.findall('<tr class="info_.*?</tr>', html, re.S)
    for course_html in courses_html:
        course = util.Course(re.search('target="_blank">(.*?)</a>', course_html, re.S).group(1).replace(' ', '').replace('\n', ''))
        url = re.search('<a href="(.*?)"', course_html, re.S).group(1)
        course.get_id(url[-6:])
        news = re.findall('red_text">(.*?)</', course_html, re.S)
        course.get_news(news)
        # To add this course into the courses_list
        courses_list.append(course)

def scan_notice(spider, course):
    """
    This is the function to scan the notices for one course, and find the ones which are unread.
    """
    #spider.gethtml('http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp?course_id=112189')
    notice_url = urls.notice + course.id
    spider.gethtml(notice_url)
    notices_html = re.findall('<tr class="tr.*?</tr>', spider.html, re.S)
    #The variable "count" counts how many unread notices have been processed, so we can ensure that we won't scan more that we expected.
    count = 0
    for notice_html in notices_html:
        if count >= course.new_notice:
           break
        flag = re.findall("<td width='20%' align='center' height=25>(.*?)</td>", notice_html, re.S)[1]
        if flag == '未读':
            count += 1
            notice_url = 'http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/' + re.search("<a  href='(.*?)'>", notice_html, re.S).group(1)
            spider.gethtml(notice_url)
            title = re.search('colspan="3">(.*?)</td>', spider.html, re.S).group(1)
            text = re.search('overflow:hidden;">(.*?)&nbsp', spider.html, re.S).group(1)
            send_to_email(title, text)

if __name__ == '__main__':

    spider = util.Spider()
    spider.login(urls.login, get_account(), get_headers())
    while True:
        courses_list = []
        html = spider.gethtml(urls.courses)
        scan_courses(html, courses_list)
        #To find the detail of each course
        for course in courses_list:
            print('----------------------------')
            print(course)

            #scan the notice list to get the notice not read
            scan_notice(spider, course)

        time.sleep(5) 
