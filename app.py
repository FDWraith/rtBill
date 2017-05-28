from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
from pymongo import MongoClient
from utils import utils, accounts
import os

#get data from secrets.txt
secrets = utils.getSecretData()

app = Flask(__name__)
app.secret_key = secrets['APP_SECRET_KEY']

URL = secrets['PROJECT_URL']
MONGO_URL = '127.0.0.1'

#connect to Mongo
connection = MongoClient('127.0.0.1')
db = connection['RT_CONGRESS_DATA']

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

#Sends an email verification
def sendVerificationEmail(email, verificationLink):
    message = Message()
    message.recipients = [ email ]
    message.subject = "Confirm Your Real Time Congress Account"
    message.html = '''
    <center>
<h1 style="font-weight: 500 ; font-family: Arial">Real Time Congress</h1>
    <p style="font-weight: 500 ; font-family: Arial">Thanks for signing up for Real Time Congress! Please press the button below to verify your account.</p>
    <br><br>
    <a href="{0}" style="padding: 1.5% ; text-decoration: none ; color: #404040; border: 1px solid black ; text-transform: uppercase ; font-weight: 500 ; font-family: Arial ; padding-left: 10% ; padding-right: 10%">Verify Email</a>
</center>
    '''.format("%s/verify/%s"%(URL, verificationLink) )
    sendEmailAsync(app, message)
        
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
    if request.form:
        #check whether we're logging in or signing up
        if 'authen' in request.form:
            if request.form['authen'] == 'login':
                user = accounts.getUser( request.form['email'], request.form['password'] ) 
                if user:
                    session['user'] = user['email']
                    session['verified'] = user['verified']
                    return redirect(url_for("home"))
                else:
                    return "ERROR"                    
            elif request.form['authen'] == 'signup':
                if accounts.createUser( request.form['email'], request.form['password'], request.form['name']):
                    user =  accounts.getUser( request.form['email'], request.form['password'] )
                    if user:
                        session['user'] = user['email']
                        session['verified'] = user['verified']
                        return ""
                return "ERROR"
            else:
                return "invalid authen arg"
        else:
            return "authen arg not found"
    else:
        return "No args found"

@app.route("/home")
def home():
    if validate():
        return render_template("home.html", verified = session['verified'] )


@app.route("/logout")
def logout():
    session.pop('verified')
    session.pop('user')
    return redirect(url_for("root"))

@app.route("/verify/<verificationLink>")
def verify(verificationLink):
    if accounts.checkVerification( session['user'], verificationLink ):
        session['verified'] = True
    return redirect( url_for('home') )


def validate():
    return 'user' and 'verified' in session

if __name__ == "__main__":
    app.debug = True
    app.run()
