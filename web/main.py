# coding = utf-8

from flask import Flask, session, redirect, url_for, request
from flask import render_template as render
from database import database
import setting
import os
import re

app = Flask(__name__)
app.debug = setting.DEBUG
app.secret_key = os.urandom(24)

@app.route('/')
@app.route('/home')
def home():
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        user = db.get_user(session['user_id'])
        courses = db.get_courses(session['user_id'])
        return render('home.html' , user = user, courses = courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = database()
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_passwd = request.form['user_passwd']
        info = db.validate_user(user_id, user_passwd)
        if len(info) == 1:
            session['login'] = 1
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            return render('login.html', message = 1)
    else:
        return render('login.html')

@app.route('/reg', methods=['GET', 'POST'])
def register():
    db = database()
    if request.method == 'POST':
        re_email = r'^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$|^(?:\+86)?(\d{3})\d{8}$|^(?:\+86)?(0\d{2,3})\d{7,8}$'
        user_id = request.form['user_id']
        user_passwd = request.form['user_passwd']
        user_email = request.form['user_email']
        # To check the validation of the user_id and user_passwd
        if not (len(user_id) >= 4 and len(user_id) <= 10 and len(user_passwd) >= 6 and len(user_passwd) <= 16):
            return render('reg.html', message = 1)

        # To the the validation of email address
        elif not re.match(re_email, user_email):
            return render('reg.html', message = 2)

        else:
            db.new_user(user_id, user_passwd, user_email)
            return redirect(url_for('home'))

    else:
        return render('reg.html')

@app.route('/logout')
def logout():
    session['login'] = 0
    session['user_id'] = None
    return redirect(url_for('home'))

@app.route('/switchon')
def switchon():
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.switch(session['user_id'], 0)
        return redirect(url_for('home'))

@app.route('/switchoff')
def switchoff():
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.switch(session['user_id'], -1)
        return redirect(url_for('home'))

@app.route('/disable/<course_id>')
def disable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.course_enable(session['user_id'], course_id, 0)
        return redirect(url_for('home'))

@app.route('/enable/<course_id>')
def enable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.course_enable(session['user_id'], course_id, 1)
        return redirect(url_for('home'))

@app.route('/course/<course_id>')
def course(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        course = db.get_course_from_id(session['user_id'], course_id)
        homework = db.get_homework(session['user_id'], course_id)
        return render('course.html', course = course, homework = homework)

@app.route('/notice_disable/<course_id>')
def notice_disable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.notice_enable(session['user_id'], course_id, 0)
        return redirect('/course/' + course_id)

@app.route('/notice_enable/<course_id>')
def notice_enable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.notice_enable(session['user_id'], course_id, 1)
        return redirect('/course/' + course_id)

@app.route('/homework_disable/<course_id>')
def homework_disable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.homework_enable(session['user_id'], course_id, 0)
        return redirect('/course/' + course_id)

@app.route('/homework_enable/<course_id>')
def homework_enable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.homework_enable(session['user_id'], course_id, 1)
        return redirect('/course/' + course_id)

@app.route('/file_disable/<course_id>')
def file_disable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.file_enable(session['user_id'], course_id, 0)
        return redirect('/course/' + course_id)

@app.route('/file_enable/<course_id>')
def file_enable(course_id):
    db = database()
    if session.get('login', 0) == 0:
        return redirect(url_for('login'))
    else:
        db.file_enable(session['user_id'], course_id, 1)
        return redirect('/course/' + course_id)


if __name__ == '__main__':
    if setting.DEBUG == True:
        app.run()
    else:
        app.run(host='0.0.0.0', port=80)
