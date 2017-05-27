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
app.secret_key = secrets['APP_SECRET_KEY']

#configure mail
app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = secrets['EMAIL_ADDRESS']
app.config['MAIL_PASSWORD'] = secrets['EMAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = ("RealTime Congress", secrets['EMAIL_ADDRESS'])

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
def root():
    if 'user' in session:
        #user is logged in, we can send them to home:
        return redirect( url_for("home") )
    else:
        if request.args:
            if 'message' in request.args:
                message = request.args['message']
                return render_template("login.html", message = message)
            else:
                print request.args
        return render_template("login.html")

@app.route("/authen", methods=['POST'])
def authen():
    if request.args:
        #check whether we're logging in or signing up
        if 'authen' in request.args:
            if request.args['authen'] == 'login':
                pass
            elif request.args['authen'] == 'signup':
                pass
            else:
                return "invalid authen arg"
        else:
            return "authen arg not found"
    else:
        return "No args found"

@app.route("/home")
def home():
    if utils.validate():
        return render_template("home.html")




if __name__ == "__main__":
    app.debug = True
    app.run()
