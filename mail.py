#-*- encoding: utf-8 -*-
import smtplib
import email
from email.mime.text import MIMEText


class mail_sender():
	def __init__(self,host,user,psw):
		self.host = host
		self.user = user
		self.loginSmtp(host,user,psw)

	def loginSmtp(self,host,user,psw):
		self.sender=smtplib.SMTP(host,timeout=30)
		self.sender.login(user,psw)

	def sendmsg(self,subject,maininfo,to_user):
		msg=MIMEText(maininfo)
		msg['Subject']=subject
		msg['From']= self.user
		msg['To']= to_user
		self.sender.sendmail(self.user,to_user,msg.as_string())
		self.sender.close()

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
    sender = mail_sender(mail_host,mail_user,mail_psw)
    sender.sendmsg(title,text,to_user)
