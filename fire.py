import os

from firebase import firebase

from mailer import Mailer

# Set up firebase
user = "notification.keralaai@gmail.com"
passw = os.environ["NOTIFICATION_EMAIL_PASS"]
# secret = os.environ["FIREBASE_SECRET"]

authentication = firebase.FirebaseAuthentication(passw, user)
print (authentication.__dict__)
firebase = firebase.FirebaseApplication('https://free-6d535.firebaseio.com/', None)
firebase.authentication = authentication
print (authentication.get_user().__dict__)

# Set up mailer
mailer = Mailer()


def get_mod_list():
    mods = []
    modlist = firebase.get('/private/mods', None)
    for mod in modlist:
        if not mod.get('mute', False):
            mods.append(mod.get('email'))
    return mods


def check_mailed_question(key):
    mailed = firebase.get('/notify/' + key + '/qmail', None)
    if mailed is True:
        return True
    else:  # can be non binary
        return False


def check_mailed_answer(key):
    mailed = firebase.get('/notify/' + key + '/amail', None)
    if mailed is True:
        return True
    else:  # can be non binary
        return False


def set_mailed_question(key):
    firebase.put('notify/' + key, 'qmail', True)


def set_mailed_answer(key):
    firebase.put('notify/' + key, 'amail', True)


def get_user_data(key):
    user = firebase.get('/users/' + key, None)
    return user


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
    threads = firebase.get('/threads', None)
    for thread, value in threads.items():
        answered = False
        posts = value.get('posts')
        title = value.get('title')
        author = value.get('user')
        if posts:
            answered = True
        question_mail(thread, title, author)
        answer_mail(thread, title, author)
        break
