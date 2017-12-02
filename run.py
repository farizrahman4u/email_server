import os
import smtplib
import email
from email.MIMEText import MIMEText

smtp_host = 'smtp.gmail.com'
smtp_port = 587

user = "notification.keralaai@gmail.com"
passw = os.environ["NOTIFICATION_EMAIL_PASS"]

server = smtplib.SMTP()
server.connect(smtp_host, smtp_port)
server.ehlo()
server.starttls()
server.login(user, passw)

fromaddr = "[Kerala AI] Notification"
tolist = ["abinsimon10@gmail.com", "fariz@logicalsteps.net"]
sub = "You just got mailed"
body = "Is this even a big deal? Well, I guess I will let you decide."

msg = email.MIMEMultipart.MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = email.Utils.COMMASPACE.join(tolist)
msg['Subject'] = sub
msg.attach(MIMEText(body))
msg.attach(MIMEText('\n- Kerala AI', 'plain'))
server.sendmail(user, tolist, msg.as_string())
