from pymongo import MongoClient
import random
import string
import utils

secrets = utils.getSecretData()

connection = MongoClient('127.0.0.1')
db = connection['RT_CONGRESS_DATA']
students = db['students']

#generate VerificationLink for a User:
def getVerificationLink():
    link = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    if db.users.count( { 'verificationLink': link } ):
        return getVerificationLink()
    else:
        return link

def checkVerification(email, link):
    if db.users.find_one( {'email': email} )['verificationLink'] == link:
        db.users.update(
            {'email': email},
            {'$set':
             {'verified':True}
            })
        return True
    return False
def createUser(email, pwd, name):
    if checkEmail( email ):
        db.users.insert(
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
    result =  db.users.find_one( {'email': email } )
    if result:
        #user is found
        if utils.hash(pwd) == result['password']:
            return True
        else:
            print "pass is wrong"
            return False
    else:
        print result
        #user is not found
        print "user not found"
        return False

def getUser(email, pwd):
    if authenticateUser(email, pwd):
        return db.users.find_one({'email':email})
    else:
        return None
