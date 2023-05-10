import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(listings):
    sender = os.environ.get('SENDER_MAIL')
    password = os.environ.get('SENDER_PASSWORD')  # 'password
    receiver = os.environ.get('RECEIVER_MAIL')

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = query + ' New Ebay Listing ACTION NEEDED!'

    body = 'New listing found. Please check the link or links below: \n' + \
        '\n'.join(listings)
    msg.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # server.set_debuglevel(1) # show what it’s doing when it sends an email
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()