#!/usr/bin/python3
import sqlite3
import main

def create_datebase(): 
    """
    This function is to initialize the database and the tables.
    """
    conn = sqlite3.connect("Courses.db")
    c = conn.cursor()
    c.execute("""
            CREATE TABLE homework 
            (id int primary key,
             IsSendToEmail int,
             IsWarning int)
            """)
    c.execute("""
            CREATE TABLE files
            (id int primary key,
             IsSendToEmail int)
            """)
    c.execute("""
            CREATE TABLE courses
            (id int primary key,
            homework int,
            files int,
            FOREIGN KEY (homework) REFERENCES homework(id),
            FOREIGN KEY (files) REFERENCES files(id))
            """)

if __name__ == '__main__':
    create_datebase()
