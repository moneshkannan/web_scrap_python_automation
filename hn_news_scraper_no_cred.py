from http import server
import requests

from bs4 import BeautifulSoup
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
from decouple import config

now = datetime.datetime.now()

content = ''


def extract_news(url):
    print('Extracting Hacker News Stories........')
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1)+' :: ' + tag.text + "\n" + '<br>')
                if tag.text != 'More' else '')
        # print(tag.prettify)
    return(cnt)


cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-------<br>')
content += ('<br><br> End of Message')

# lets sends email
print("composing email.....")

SERVER = config('SERVER')
PORT = 587  # port number
FROM = config('FROM')  # from email id
TO = config('TO')  # to email id
PASS = config('PASS')  # password

# fp = open(filename, 'rb')
# craete a text/plain message
# msg = MIMEText('')

msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + \
    str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
print('Initiating server..............')
server = smtplib.SMTP(SERVER, PORT)
# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent.....')
server.quit()
