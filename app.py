from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
from pymongo import MongoClient
from utils import utils, accounts
import os

connection = MongoClient("127.0.0.1")
db = connection['RTCONGRESS_DATA']

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"





if __name__ == "__main__":
    app.debug = True
    app.run()
