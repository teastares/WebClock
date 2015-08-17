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


