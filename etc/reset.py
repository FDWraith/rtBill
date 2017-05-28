from pymongo import MongoClient

connection = MongoClient("127.0.0.1")
db = connection["RT_CONGRESS_DATA"]

def reset():
    db.students.drop()

reset()
