#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
import requests
import sys
import os.path

ip_request = requests.get('http://ipecho.net/plain')

if ip_request.status_code != 200:
    print ("Failed to request site") 
    print (ip_request.status_code)
    sys.exit()

ip = ip_request.text

f = open('/home/pi/e-mail/last_ip','r+')
last_ip = f.readline()

print (ip)
if ip != last_ip:
    gmailUser = os.environ['GMAIL_EMAIL']
    gmailPassword = os.environ['GMAIL_PASS']
    print (gmailUser, gmailPassword)
    smtpserver=smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()  
    smtpserver.starttls()  
    smtpserver.ehlo()
    smtpserver.login(gmailUser, gmailPassword)
    msg = MIMEText(ip)
    msg['Subject'] = 'Current ip'
    msg['From'] = gmailUser
    To=os.environ['TO_EMAIL']
    print (To)
    msg['To'] = To
    smtpserver.sendmail(gmailUser, To, msg.as_string())
    smtpserver.quit()


    f.seek(0)
    f.truncate()
    f.write(ip)

f.close()
