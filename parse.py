#!/usr/bin/python3
from bs4 import BeautifulSoup

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
        name = info.contents[0].replace(' ','').replace('\n','')
        course_id = int(url[-6:])
        yield(course_id, name, url)

def get_news(html):
    soup = BeautifulSoup(html, "html.parser")
    for course in soup.find_all('tr', class_ = ['info_tr', 'info_tr2']):
        course_id = int(course.find('a')['href'][-6:])
        info = [course_id]
        news = course.find_all('td')[1:]
        for item in news:
            info.append(int(item.get_text()[0]))
        yield(info)
