from pymongo import MongoClient
import random
import string
import utils

secrets = utils.getSecretData()

connection = MongoClient('127.0.0.1')
db = connection['RTCONGRESS_DATA']

#generate VerificationLink for a User:
def getVerificationLink():
    link = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    if db.users.count( { 'verificationLink': link } ):
        return getVerificationLink()
    else:
        return link

def createUser(email, pwd, name):
    if checkEmail( email ):
        db.users.insert_one(
            {
                'email': email,
                'password': utils.hash(pwd),
                'name': name,
                'verificationLink': getVerificationLink(),
                'verified': False,
                'interests': [ ],
                'saved_bills': [ ]
            })
        return True
    else:
        return False

def checkEmail( email ):
    return not db.users.find({'email':email})

def authenticateUser(email, pwd):
    with db.users.find_one( {'email': email } ) as result:
        if result:
            #user is found
            if utils.hash(pwd) == result['password']:
                return True
            else:
                return False
        else:
            #user is not found
            return False

def getUser(email, pwd):
    if authenticateUser(email, pwd):
        return db.user.find_one({'email':email})
    else:
        return None
