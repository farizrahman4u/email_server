import os
import smtplib
from email.mime.multipart import MIMEMultipart as MM
from email.mime.text import MIMEText as MT

smtp_host = 'smtp.gmail.com'
smtp_port = 587

user = "notification.keralaai@gmail.com"
passw = os.environ["NOTIFICATION_EMAIL_PASS"]


class Mailer:
    def __init__(self):
        self.server = smtplib.SMTP(smtp_host, smtp_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(user, passw)

    def _mail(self, tolist, subject, body):
        fromaddr = "[Kerala AI Initiative] Notification"

        msg = MM()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(tolist)
        msg['Subject'] = subject
        msg.attach(MT(body))
        msg.attach(MT('\n- Kerala AI Initiative', 'plain'))
        self.server.sendmail(user, tolist, msg.as_string())

    def mail(self, tolist, subject, body):
        try:
            if isinstance(tolist, str):
                self._mail([tolist], subject, body)
            else:
                self._mail(tolist, subject, body)
            return True
        except Exception as e:
            print (e)
            return False


if __name__ == '__main__':
    mailer = Mailer()
    to = "abinsimon10@gmail.com"
    sub = "You just got mailed"
    body = "Is this even a big deal? Well, I guess I will let you decide."
    mailer.mail(to, sub, body)
