import os
import datetime
import pyrebase
from mailer import Mailer

# Set up firebase
config = {
    "apiKey": "AIzaSyCV_wkx8gh3NzFuctl6AdSZ10ZK1qkv8qY",
    "authDomain": "free-6d535.firebaseapp.com",
    "databaseURL": "https://free-6d535.firebaseio.com",
    "storageBucket": "free-6d535.appspot.com",
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = "notification.keralaai@gmail.com"
passw = os.environ["NOTIFICATION_EMAIL_PASS"]
login_time = datetime.datetime.now()
user = auth.sign_in_with_email_and_password(user, passw)
db = firebase.database()

# Set up mailer
mailer = Mailer()


def get_mod_list():
    mods = []
    modlist = db.child("private").child("mods").get(user['idToken']).val()
    for mod in modlist:
        if not mod.get('mute', False):
            mods.append(mod.get('email'))
    return mods


def check_mailed_question(key):
    mailed = db.child("notify").child(key).child("qmail").get(user['idToken']).val()
    if mailed is True:
        return True
    else:  # can be non binary
        return False


def check_mailed_answer(key):
    mailed = db.child("notify").child(key).child("amail").get(user['idToken']).val()
    if mailed is True:
        return True
    else:  # can be non binary
        return False


def set_mailed_question(key):
    db.child("notify").child(key).child("qmail").set(True, user['idToken'])


def set_mailed_answer(key):
    db.child("notify").child(key).child("amail").set(True, user['idToken'])


def get_user_data(key):
    u = db.child("users").child(key).get(user['idToken']).val()
    return u


def get_question_mail_message(title, user):
    user = get_user_data(user)
    message = "New questions \"{}\" from \"{}\" ".format(title, user.get('displayName'))
    return message


def get_answer_mail_message(title):
    message = "Your question \"{}\" has been answered.".format(title)
    return message


def question_mail(key, title, author):
    if not check_mailed_question(key):
        toaddr = get_mod_list()
        subject = "New question"
        message = get_question_mail_message(title, author)
        OK = mailer.mail(toaddr, subject, message)
        if OK:  # maybe it will work next time
            set_mailed_question(key)


def answer_mail(key, title, user):
    if not check_mailed_answer(key):
        user = get_user_data(user)
        toaddr = user.get('email')
        message = get_answer_mail_message(title)
        subject = "Question answered"
        OK = mailer.mail(toaddr, subject, message)
        if OK:  # maybe it will work next time
            set_mailed_answer(key)


if __name__ == '__main__':
    threads = db.child("threads").get(user['idToken']).val()
    for thread, value in threads.items():
        # in case auth timed out
        if ((datetime.datetime.now() - login_time) > datetime.timedelta(minutes=45)):
            login_time = datetime.datetime.now()
            user = auth.refresh(user['refreshToken'])

        answered = False
        posts = value.get('posts')
        title = value.get('title')
        author = value.get('user')
        if posts:
            answered = True
        question_mail(thread, title, author)
        answer_mail(thread, title, author)
