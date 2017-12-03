import os
import smtplib
import email
from email.mime.multipart import MIMEMultipart as MM
from email.mime.text import MIMEText as MT

smtp_host = 'smtp.gmail.com'
smtp_port = 587

user = "notification.keralaai@gmail.com"
passw = os.environ["NOTIFICATION_EMAIL_PASS"]


class Mailer:
    def __init__(self):
        self.server = smtplib.SMTP()
        self.server.connect(smtp_host, smtp_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(user, passw)

    def _mail(self, to_address, subject, body):
        fromaddr = "[Kerala AI Initiative] Notification"
        tolist = to_address  # expects a list

        msg = MM()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(tolist)
        msg['Subject'] = subject
        msg.attach(MT(body))
        msg.attach(MT('\n- Kerala AI', 'plain'))
        self.server.sendmail(user, tolist, msg.as_string())

    def mail(self, to_address, subject, body):
        try:
            self._mail([to_address], subject, body)
        except Exception as e:
            print (e)


if __name__ == '__main__':
    mailer = Mailer()
    to = "abinsimon10@gmail.com"
    sub = "You just got mailed"
    body = "Is this even a big deal? Well, I guess I will let you decide."
    mailer.mail(to, sub, body)
