#!/usr/bin/python3
"""
If Enable_Mail = 0, we will disable some functions, and use something like print to replace it.
elif Enable_Mail = 1, we will enable the some function.

Functions include:
    ** send_to_email() in mail.py **
"""
Enable_Mail = 0


"""
If Enable_Hw = 0, we will not scan the homework for each course.
elif Enable_Hw = 1, we will enable the functions.
"""
Enable_Hw = 1

"""
If Enable_Notice = 0, we will not scan the notices for each course.
elif Enable_Notice = 1, we will enable the functions.
elif Enable_Notice = 2, we will scan all the notices, not only the unread notice.
"""
Enable_Notice = 0


"""
If Enable_File = 0, we will not scan the Files for each course.
elif Enable_File = 1, we will enable the functions.
"""
Enable_File = 1

"""
Idle_Time is the number of seconds
Between two scannings.
"""
Idle_Time = 60

"""
Here describes the information of database.
"""
db_host = 'localhost'
db_user = 'webclock'
db_passwd = 'webclockv1.2'
db_database = 'webclock'
db_port = 3306
db_charset = 'utf8'
