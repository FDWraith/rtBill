from pymongo import MongoClient
import hashlib

connection = MongoClient('127.0.0.1')
db = connection['RT_CONGRESS_DATA']

def hash( value ):
    return hashlib.sha256(value).hexdigest()

def create():
    db.users.insert(
        {
        'email': 'kevinzhang3702@gmail.com',
        'password': hash('admin'),
        'name': 'kevin',
        'verificationLink': 'rip',
        'verified': True,
        'interests': [ ],
        'saved_bills': [ ]
    })

create()
