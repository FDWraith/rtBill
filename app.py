from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
from pymongo import MongoClient
from utils import utils
import os

#connect to Mongo
connection = MongoClient("127.0.0.1")
db = connection['RTCONGRESS_DATA']

#get data from secrets.txt
secrets = utils.getSecretData()

app = Flask(__name__)

#configure mail
app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = secrets['email']
app.config['MAIL_PASSWORD'] = secrets['email-password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = ("StuyCS Code Review", secrets['email'])

#initialize mail
mail = Mail(app)

#here is async wrapper for mail
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

#forces flask-mail to send email asynchronously
@async
def sendEmailAsync(app, message):
    with app.app_context():
        mail.send(message)

@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"





if __name__ == "__main__":
    app.debug = True
    app.run()
