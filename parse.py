#!/usr/bin/python3
from bs4 import BeautifulSoup
import setting
import re

def get_courses(html):
    """
    Get the information for each course,
    includes the name, url and id for a course
    """
    soup = BeautifulSoup(html, "html.parser")
    for course in soup.find_all('tr', class_ = ['info_tr', 'info_tr2']):
        info = course.find('a')
        #NOTE THE NEW WEB
        url = info['href']
        name = re.sub(r'[ \n\r\t]', '',info.contents[0])[:-15]
        course_id = url[-6:]
        info = (course_id, name, url)
        yield(info)

def get_news(html):
    """
    From the courses web, get the number of the
    notice, new file and new homework for each
    course.
    """
    soup = BeautifulSoup(html, "html.parser")
    for course in soup.find_all('tr', class_ = ['info_tr', 'info_tr2']):
        course_id = course.find('a')['href'][-6:]
        info = [course_id]
        news = course.find_all('td')[1:]
        for item in news:
            info.append(int(item.get_text()[0]))
        yield(info)

def get_newhomework(html):
    """
    For one course, get all the homework,
    include url, homework_id,
    title, deadline and state.
    """
    soup = BeautifulSoup(html, "html.parser")
    for homework in soup.find_all('tr', class_ = ['tr1', 'tr2']):
        url = homework.find('a')['href']
        homework_id = re.search('\d{6}', url).group(0)
        title = homework.find('a').get_text()
        state = homework.find('td', width = ['15%']).get_text()
        state = re.sub(r'[ \n\r\t]', '',state)
        deadline = homework.find_all('td', width = ['10%'])[1].get_text()
        info = [homework_id, url, title, state, deadline]
        yield(info)

def get_homeworkdetail(html):
    """
    For one homework, to get its instruction.
    """
    soup = BeautifulSoup(html, "html.parser")
    info = soup.find('textarea').get_text()
    return(info)

def get_newnotice(html, num_unread):
    """
    For one course, get all the unread(if setting.Enable_Notice == 1)
    notices or all the notices(if setting.Enable_Notice == 2)
    """
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for notice in soup.find_all('tr', class_ = ['tr1', 'tr2']):
        if setting.Enable_Notice == 1 and count >= num_unread:
            break
        a = notice.find('a')
        url = a['href']
        title = a.get_text()
        author = notice.find('td', width = ["15%"]).get_text()
        state = notice.find_all('td', width = ["20%"])[1].get_text()
        state = re.sub(r'[ \n\r\t]', '',state)
        if setting.Enable_Notice == 2 or state == '未读':
            count += 1
            info = (url, title, author)
            yield(info)

def get_newfile(html, num_newfile):
    """
    For one course, get all the new file (if setting.Enable_File == 1)
    info or all the new file info (if setting.Enable_File == 2)
    """
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for newfile in soup.find_all('tr', class_ = ['tr1', 'tr2']):
        if setting.Enable_File == 1 and count >= num_newfile:
            break
        a = newfile.find('a')
        url = a['href']
        title = a.get_text()
        description = newfile.find('td', width = ["300"]).get_text()
        if description == '':
            description = 'No description!'
        filesize = newfile.find('td', width = ["80"], align = ["center"]).get_text()
        state = newfile.find_all('td', width = ["100"])[1].get_text()
        state = re.sub(r'[ \n\r\t]', '',state)
        if setting.Enable_Notice == 2 or state == '新文件':
            count += 1
            info = (url, title, description, filesize)
            yield(info)
            
def get_noticedetail(html):
    soup = BeautifulSoup(html, "html.parser")
    info = soup.find_all('td', class_ = ["tr_l2"])[1].get_text()
    return(info)
