#!/usr/bin/python3
"""
If Enable_Mail = 0, we will disable some functions, and use something like print to replace it.
elif Enable_Mail = 1, we will enable the some function.

Functions include:
    ** send_to_email() in mail.py **
"""
Enable_Mail = 1

"""
Idle_Time is the number of seconds
Between two scannings.
"""
Idle_Time = 0

"""
Here describes the information of database.
"""
db_host = 'localhost'
db_user = 'webclock'
db_passwd = 'webclockv1.2'
db_database = 'webclock'
db_port = 3306
db_charset = 'utf8'
